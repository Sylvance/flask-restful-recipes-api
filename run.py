""" The Application's Entry Point"""
import os
from code import create_app
app = create_app()

if __name__ == '__main__':
	app.run(debug=True)
