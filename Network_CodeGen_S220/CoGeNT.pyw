                     
import htmlPy
from back_end import BackEnd
from back_end import app


if __name__ == "__main__":
    app.bind(BackEnd())
    app.start()
 