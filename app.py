#python lib
import os
import commands
import re
#flask lib
from flaskext.enterprise import Enterprise
from flask import Flask, render_template

#config Flask
app = Flask(__name__)

#config Flask Enterprise
enterprise = Enterprise(app)
String = enterprise._sp.String
Integer = enterprise._sp.Integer
Boolean = enterprise._sp.Boolean
Array = enterprise._scls.Array

r = re.compile("(cd|chdir)\s+(.*)")

class Chdir:
      def __init__( self, newPath ):  
        self.savedPath = os.getcwd()
        os.chdir(newPath)

      def __del__( self ):
        os.chdir( self.savedPath )

class Service(enterprise.SOAPService):
    """Soap Service Class
    
    Attributes:
        __soap_target_namespace__ : namespace for soap service
        __soap_server_address__ : address of soap service
    """
    __soap_target_namespace__ = 's1011435'
    __soap_server_address__ = '/soap'

    @enterprise.soap(String, _returns=String)
    def command(self, c):
        """ Function that executes a given Linux command

        Args:
            c : string

        Returns:
            return multiple lines of string
        """
        cd = r.match(c)
        if cd:
            os.chdir(cd.group(2))
            return
        return commands.getoutput(c)

@app.route('/')
def pageIndex():
    """ The index page
    """
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    """ Error 404
    """
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    """ Error 403
    """
    return render_template("403.html"), 403

@app.errorhandler(410)
def gone(e):
    """ Error 410
    """
    return render_template("410.html"), 410

@app.errorhandler(500)
def internal_server_error(e):
    """ Error 500
    """
    return render_template("500.html"), 500

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='127.0.0.1', port=port)
