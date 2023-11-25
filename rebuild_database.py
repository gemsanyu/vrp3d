from data.database import Database


def run():
    Database.Initialize()
    Database.Rebuild()    

if __name__ == "__main__":
    run()