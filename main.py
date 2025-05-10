from app.ui.console import main_menu
from app.data.database import init_db
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    init_db()
    main_menu()
