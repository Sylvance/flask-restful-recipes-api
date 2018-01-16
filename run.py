""" The Application's Entry Point"""
import os
from code import create_app
app = create_app()

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(port=port, debug=True)
