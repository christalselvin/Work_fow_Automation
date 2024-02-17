"""App entry point."""
import sys
from flask_cors import CORS
sys.path.append("C:\\Users\\Admin\\PycharmProjects")

from autointellimini import create_app
app = create_app()
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8988)
