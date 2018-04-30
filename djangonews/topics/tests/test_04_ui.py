import pytest
import os

try:
    from selenium.webdriver.common.action_chains import ActionChains
except Exception as e:
    pass

import random

protocol = 'https://' if os.environ.get('USING_HTTPS') == 'yes' else 'http://'
used_domain = os.environ.get('USED_DOMAIN') or 'localhost:8000'
site_index_url = '{}{}/'.format(protocol, used_domain)

@pytest.mark.skip
def test_ui_login(selenium):
    selenium.get(site_index_url)
    login_link = selenium.find_element_by_id('login-link')
    login_link.click()
    login_form = selenium.find_element_by_id('login-form')
    username_field = selenium.find_element_by_id('id_username')
    password_field = selenium.find_element_by_id('id_password')
    username_field.send_keys('hamzael')
    password_field.send_keys('elpass')
    login_btn = selenium.find_element_by_id('login-btn')
    login_btn.click()
    selenium.implicitly_wait(2)
    assert selenium.current_url == site_index_url
    assert selenium.find_element_by_id('logout-link')

@pytest.mark.skip
def test_ui_logout(selenium):
    test_ui_login(selenium)
    assert selenium.current_url == site_index_url
    welcome_menu = selenium.find_element_by_id('welcome-menu')
    ActionChains(selenium).move_to_element(welcome_menu)
    logout_link = selenium.find_element_by_id('logout-link')
    logout_url = logout_link.get_attribute('href')
    selenium.get(logout_url)
    selenium.implicitly_wait(5)
    assert selenium.find_element_by_id('login-link')

@pytest.mark.skip
def test_ui_browse_to_detail_topic_page(selenium):
    selenium.get(site_index_url)
    # Wait for 5 seconds until the Ajax Calls finish
    selenium.implicitly_wait(5) 
    article_links = selenium.find_elements_by_class_name('article-link')
    if len(article_links) == 0:
        assert 1==0, 'There are no Topics to browse to :/'
    else:
        # Click on a random article
        article_links[random.randint(0,len(article_links)-1)].click()
        assert 'topics/' in selenium.current_url
        assert selenium.find_element_by_class_name('topic-detail')

@pytest.mark.skip
def test_ui_logged_can_upvote_topic(selenium):
    test_ui_login(selenium)
    max_loop = 0
    while True: # loop in case the topic is already upvoted in the past
        test_ui_browse_to_detail_topic_page(selenium)
        upvote_btn = selenium.find_element_by_id('upvote-btn')
        if not upvote_btn.get_attribute('class').strip() == 'upvoted':
            break
        elif max_loop == 50:
            assert 1 == 0, 'All Topics were upvoted, cant test this case' # Stop the test
        max_loop += 1
    # Click on Upvote button
    upvote_btn.click()
    # Check if the upvoted class was added
    selenium.implicitly_wait(3)
    upvote_btn = selenium.find_element_by_id('upvote-btn')
    assert upvote_btn.get_attribute('class').strip() == 'upvoted'

@pytest.mark.skip
def test_ui_logged_can_comment_on_topic(selenium):
    # Login
    test_ui_login(selenium)
    # Browse to a topic page
    test_ui_browse_to_detail_topic_page(selenium)
    # Get current number of comment to know later if the comment was added
    nbr_comments_before = len(selenium.find_elements_by_class_name('comment'))
    # Show the comment box
    comment_btn = selenium.find_element_by_id('write-com-btn')
    comment_btn.click()
    # Write comment in the TextArea
    comment_area = selenium.find_element_by_id('id_content')
    comment_area.send_keys('Watch out ! Selenium Bot is testing here !')
    # Click to submit the comment
    submit_comment_btn = selenium.find_element_by_id('submit-com-btn')
    submit_comment_btn.click()
    # Get the new number of comments
    selenium.implicitly_wait(3)
    nbr_comments_after = len(selenium.find_elements_by_class_name('comment'))
    # Compare them
    assert nbr_comments_after - nbr_comments_before == 1

@pytest.mark.skip
def test_ui_topics_ajax_pagination(selenium):
    selenium.get(site_index_url)
    more_btn = selenium.find_element_by_id('more-btn')
    nbr_topics_before = len(selenium.find_elements_by_class_name('topic-block'))
    more_btn.click()
    selenium.implicitly_wait(5)
    nbr_topics_after = len(selenium.find_elements_by_class_name('topic-block'))
    assert nbr_topics_before < nbr_topics_after

@pytest.mark.skip
def test_ui_logged_can_write_topic(selenium):
    # Login
    test_ui_login(selenium)
    # Browse to "write topic" page
    selenium.get(site_index_url + 'topics/new')
    # Fill Form
    title_input = selenium.find_element_by_id('id_title')
    title_input.send_keys('Selenium Test')
    slug_input = selenium.find_element_by_id('id_slug')
    slug_input.send_keys('selenium-test')
    selenium.switch_to_frame('id_content_ifr')
    selenium.find_element_by_id("tinymce").clear()
    selenium.find_element_by_id("tinymce").send_keys('Some text here')
    selenium.switch_to_default_content()
    # Submit
    submit_btn = selenium.find_element_by_id('write-topic-btn')
    submit_btn.click()
