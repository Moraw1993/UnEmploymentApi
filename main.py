############## IMPORT PACKAGES ##################
import argparse
from logger import get_logger
from utilities import ConfigManager, delete_logs
from dotenv import load_dotenv
from downloader import UnemploymentDownloader


### Validate functions for type argument
def validate_year(year):
    if len(year) != 4 or not year.isdigit():
        raise argparse.ArgumentTypeError("Year must have 4 digits.")
    year_int = int(year)
    if year_int < 2000 or year_int > 2099:
        raise argparse.ArgumentTypeError("Year must be in the range 2000-2099.")
    return year


def validate_month(month):
    if len(month) != 2 or not month.isdigit():
        raise argparse.ArgumentTypeError("Month must have 2 digits.")
    return month


def validate_add_year(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError("The given value must be a positive value")
    return int(value)


def main():
    ### load data for .env
    load_dotenv()

    ### init parser
    parser = argparse.ArgumentParser(description="Data Extraction")

    ### create parser group for the call config downloader
    config_group = parser.add_argument_group("Get data using config.json")
    config_group.add_argument(
        "--config",
        help="Get data for years and months from the config.json",
        metavar="CONFIG_FILE",
        choices=["config.json"],
    )

    ### create parser group for the specific date downloader
    data_group = parser.add_argument_group("Get data for the specific date")
    data_group.add_argument(
        "--year",
        type=validate_year,
        help="Year from range (2000-2099) to extract data.\nThis argument can be used alone",
    )
    data_group.add_argument(
        "--month",
        type=validate_month,
        help="Month to extract data.\nThis argument must be used with --year",
        choices=[
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
        ],
    )

    ### create parser group for the add new year and months to the config file
    add_year_group = parser.add_argument_group("Add Year")
    add_year_group.add_argument(
        "--add_year",
        help="Add the next year with all months set to False in the config.json",
        action="store",
        type=validate_add_year,
        metavar="NUMBER_OF_YEARS",
    )

    ### parse groups
    args = parser.parse_args()

    ### check combination of optional arguments
    if (args.config and (args.year or args.month or args.add_year)) or (
        args.add_year and (args.year or args.month)
    ):
        parser.error(
            "Please provide either a config file, or year and month, or add_year, but not in combination."
        )

    if args.config:
        ETLclient = UnemploymentDownloader(config=args.config)
    elif args.year or args.month:
        if not args.year:
            parser.error("Please provide year argument")
        ETLclient = UnemploymentDownloader(year=args.year, month=args.month)
    elif args.add_year:
        config_manager = ConfigManager()
        config_manager.load_config("config.json")
        for _ in range(args.add_year):
            config_manager.add_next_year("config.json")
        exit()
    else:
        parser.error("Please provide either a config file or year and month.")

    try:
        ### init logger
        logger = get_logger(__name__)
        ## delete log older then 30 days
        delete_logs("logs")
        logger.info(f"Start program with the arguments: {args}")
        ### start ETL
        ETLclient.run_ETL()
        ### end program
        logger.info(f"The program has ended successfully.")
    except:
        logger.exception(
            "an error occurred that was not handled while the application was running",
        )


if __name__ == "__main__":
    main()
