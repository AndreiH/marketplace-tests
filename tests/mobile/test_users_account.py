#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from unittestzero import Assert

from pages.mobile.home import Home


class TestAccounts():

    @pytest.mark.nondestructive
    def test_user_can_login_and_logout(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        settings_page = home_page.header.click_settings()
        settings_page.login(user="default")

        Assert.equal(settings_page.email_text, mozwebqa.credentials["default"]["email"])

        settings_page.click_logout()
        Assert.true(settings_page.is_sign_in_visible)

    @pytest.mark.nondestructive
    def test_user_sign_in_from_my_apps(self, mozwebqa):

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        settings_page = home_page.header.click_settings()
        my_apps = settings_page.click_my_apps(logged_in=False)

        my_apps.login(user="default")
        Assert.true(my_apps.are_my_app_visible)

    @pytest.mark.nondestructive
    def test_user_can_go_back_from_settings_page(self, mozwebqa):
        """
        https://bugzilla.mozilla.org/show_bug.cgi?id=795185#c11
        """

        home_page = Home(mozwebqa)
        home_page.go_to_homepage()

        settings_page = home_page.header.click_settings()
        settings_page.login(user="default")
        Assert.equal(settings_page.email_text, mozwebqa.credentials["default"]["email"])

        settings_page.click_my_apps()
        settings_page.header.click_homepage_back()

        Assert.true(home_page.is_new_category_tab_visible)
