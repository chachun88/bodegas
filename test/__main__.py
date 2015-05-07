import unittest

from tests.model_enterprise_test import ModelEnterpriseTest
from tests.model_users_test import ModelUsersTest
from tests.model_business_test import ModelBusinessTest
from tests.model_address_test import ModelAddressTest

from config import *
from lp.globals import *
from tornado.options import define

define("protocol", default="https", help="run on the given port", type=str)

define("db_name", default=ONTEST_DB_NAME, help="", type=str)
define("db_user", default=ONTEST_USER, help="", type=str)
define("db_host", default=ONTEST_HOST, help="", type=str)
define("db_password", default=ONTEST_PASSWORD, help="", type=str)

if __name__ == "__main__":
    unittest.main()
