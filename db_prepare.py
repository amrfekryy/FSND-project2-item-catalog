# add database directory to python modules path.
import sys
sys.path.append("./database/")

from database import db_setup, db_populate, db_print


def main():

    # setup database
    db_setup.main()
    print("------------------------")
    # populate databae with initial data
    db_populate.main()
    print("------------------------")
    # print database contents
    db_print.main()
    print("------------------------")

    print("\nDatabase has been prepared\n")


if __name__ == '__main__':
    main()
