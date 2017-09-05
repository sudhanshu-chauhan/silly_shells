import os


# LOG DIRECTORY
LOG_DIR = os.path.join(os.path.dirname(__file__),
                       os.pardir,
                       os.pardir,
                       os.pardir,
                       "logs")


# JWT SECRET KEY
JWT_SECRET = 'mC0~RCmb+(Ks"DOcS%M)rXu+N>?d2$3vySw}bfcV|eAAQhWFa3X1{L1|,Ym<-|+'

# DATABASE URL
DATABASE_URL = 'postgresql://postgres:random123@localhost/silly_shells'
