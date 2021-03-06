#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from selenium.webdriver.common.by import By

from pages.mobile.base import Base


class Reviews(Base):
    """
    Page with all reviews of an app.
    """

    _review_list_locator = (By.CSS_SELECTOR, '.review')
    _detete_review_button_locator = (By.CSS_SELECTOR, '.delete.post')

    @property
    def is_reviews_list_visible(self):
        return self.is_element_visible(*self._review_list_locator)

    def go_to_reviews_page(self, app):
        self.selenium.get('%s/app/%s/ratings' % (self.base_url, app))
        self.app = app

    def wait_for_reviews_visible(self):
        self.wait_for_element_present(*self._review_list_locator)

    def delete_review(self):
        self.selenium.find_element(*self._detete_review_button_locator).click()

    @property
    def _page_title(self):
        return 'Reviews for %s | Firefox Marketplace' % self.app

    @property
    def reviews(self):
        """Returns review object with index."""
        return [self.ReviewSnippet(self.testsetup, web_element) for web_element in self.selenium.find_elements(*self._review_list_locator)]

    class ReviewSnippet(Base):

            _review_text_locator = (By.CSS_SELECTOR, '.body')
            _review_rating_locator = (By.CSS_SELECTOR, 'span')
            _review_author_locator = (By.CSS_SELECTOR, 'span.byline > strong')
            _delete_review_locator = (By.CSS_SELECTOR, '.delete')

            def __init__(self, testsetup, element):
                Base.__init__(self, testsetup)
                self._root_element = element

            @property
            def text(self):
                return self._root_element.find_element(*self._review_text_locator).text

            @property
            def rating(self):
                return int(self._root_element.find_element(*self._review_rating_locator).get_attribute('class')[-1])

            def delete(self):
                self.wait_for_element_visible(*self._delete_review_locator)
                self._root_element.find_element(*self._delete_review_locator).click()

            @property
            def author(self):
                return self._root_element.find_element(*self._review_author_locator).text

            @property
            def is_review_visible(self):
                return self.is_element_visible(*self._review_text_locator)
