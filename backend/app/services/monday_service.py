import requests
from typing import List, Dict, Any, Tuple
from app.config import settings
from app.utils.logger import logger
from app.data.mock_fixtures import MOCK_DEALS_RAW, MOCK_WORK_ORDERS_RAW

MONDAY_GRAPHQL_URL = "https://api.monday.com/v2"

class MondayService:
    def __init__(self):
        self.api_token = settings.MONDAY_API_TOKEN
        self.deals_board_id = settings.MONDAY_DEALS_BOARD_ID
        self.work_orders_board_id = settings.MONDAY_WORK_ORDERS_BOARD_ID
        
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            "API-Version": "2023-10"
        }
        
    def _execute_query(self, query: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.api_token:
            raise ValueError("Monday.com API Token is not configured.")
            
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
            
        try:
            response = requests.post(
                MONDAY_GRAPHQL_URL, 
                json=payload, 
                headers=self.headers, 
                timeout=12
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                error_msg = "; ".join([e.get("message", "Unknown GraphQL error") for e in data["errors"]])
                logger.error(f"Monday GraphQL Error: {error_msg}")
                raise Exception(f"Monday API Error: {error_msg}")
                
            return data.get("data", {})
        except requests.exceptions.Timeout:
            logger.error("Monday.com API connection timed out.")
            raise Exception("Monday.com API timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Monday HTTP request failed: {str(e)}")
            raise Exception(f"Failed to communicate with Monday.com API: {str(e)}")

    def fetch_board_items_raw(self, board_id: str) -> List[Dict[str, Any]]:
        query = """
        query ($boardId: [ID!], $cursor: String) {
          boards(ids: $boardId) {
            id
            name
            items_page(limit: 100, cursor: $cursor) {
              cursor
              items {
                id
                name
                column_values {
                  id
                  text
                  value
                  column {
                    title
                  }
                }
              }
            }
          }
        }
        """
        
        all_raw_items = []
        cursor = None
        
        while True:
            variables = {"boardId": [board_id], "cursor": cursor}
            res_data = self._execute_query(query, variables)
            boards = res_data.get("boards", [])
            
            if not boards:
                break
                
            board = boards[0]
            items_page = board.get("items_page", {})
            items = items_page.get("items", [])
            
            for item in items:
                raw_dict = {
                    "id": item.get("id"),
                    "name": item.get("name")
                }
                
                # Extract columns by column title or text
                for cv in item.get("column_values", []):
                    title = (cv.get("column", {}).get("title") or cv.get("id") or "").lower().strip()
                    val_text = cv.get("text")
                    
                    if "sector" in title:
                        raw_dict["sector"] = val_text
                    elif any(k in title for k in ("deal size", "amount", "value", "contract")):
                        raw_dict["deal_size"] = val_text
                        raw_dict["contract_value"] = val_text
                    elif any(k in title for k in ("stage", "deal stage")):
                        raw_dict["stage"] = val_text
                    elif "status" in title:
                        raw_dict["status"] = val_text
                    elif any(k in title for k in ("expected close", "close date", "date")):
                        raw_dict["expected_close_date"] = val_text
                    elif "start date" in title:
                        raw_dict["start_date"] = val_text
                    elif any(k in title for k in ("target completion", "completion date", "due date")):
                        raw_dict["target_completion_date"] = val_text
                    elif "deal name" in title or "related deal" in title:
                        raw_dict["deal_name"] = val_text
                        
                all_raw_items.append(raw_dict)
                
            cursor = items_page.get("cursor")
            if not cursor or len(items) == 0:
                break
                
        return all_raw_items

    def get_deals_raw(self, force_demo: bool = False) -> List[Dict[str, Any]]:
        if force_demo or settings.DEMO_MODE:
            logger.info("Using Demo Mode mock dataset for Deals board.")
            return MOCK_DEALS_RAW
            
        try:
            items = self.fetch_board_items_raw(self.deals_board_id)
            logger.info(f"Fetched {len(items)} deals directly from Monday.com board ID {self.deals_board_id}")
            return items
        except Exception as e:
            logger.error(f"Failed to fetch live Deals from Monday API: {str(e)}")
            raise Exception(f"Unable to retrieve the Deals board from Monday.com: {str(e)}")

    def get_work_orders_raw(self, force_demo: bool = False) -> List[Dict[str, Any]]:
        if force_demo or settings.DEMO_MODE:
            logger.info("Using Demo Mode mock dataset for Work Orders board.")
            return MOCK_WORK_ORDERS_RAW
            
        try:
            items = self.fetch_board_items_raw(self.work_orders_board_id)
            logger.info(f"Fetched {len(items)} work orders directly from Monday.com board ID {self.work_orders_board_id}")
            return items
        except Exception as e:
            logger.error(f"Failed to fetch live Work Orders from Monday API: {str(e)}")
            raise Exception(f"Unable to retrieve the Work Orders board from Monday.com: {str(e)}")

    def check_connection(self) -> Tuple[bool, str]:
        if not settings.has_valid_monday_creds:
            return False, "Monday.com API token or Board IDs are not configured. Currently running in Demo Mode."
            
        query = "query { me { id name email } }"
        try:
            res = self._execute_query(query)
            user_info = res.get("me", {})
            user_name = user_info.get("name", "User")
            return True, f"Connected successfully to Monday.com as {user_name}."
        except Exception as e:
            return False, f"Monday.com API Connection failed: {str(e)}"

monday_service = MondayService()
