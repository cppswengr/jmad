from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from .utils import create_test_data


class StaffTestCase(LiveServerTestCase):

    def setUp(self):

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

        self.admin_user = \
            get_user_model().objects.create_superuser(
                username='bran',
                email='bran@eVantageGroup.com',
                password='august'
            )

        create_test_data()

    def tearDown(self):
        self.browser.quit()

    def test_staff_can_add_content(self):
        """
        Tests that a 'staff' user can access the admin and
        add Albums, Tracks, and Solos
        """
        # Bill would like to add a record and a number of
        # solos to JMAD. He visits the admin site
        admin_root = self.browser.get(
            self.live_server_url + '/admin/'
        )

        # He can tell he's in the right place because of the
        # title of the page
        self.assertEqual(self.browser.title,
                         'Log in | Django site admin')

        # He enters his username and password and submits the
        # form to log in
        login_form = self.browser.find_element_by_id(
            'login-form')
        login_form.find_element_by_name('username'). \
            send_keys('bran')
        login_form.find_element_by_name('password'). \
            send_keys('august')
        login_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He sees links to Albums, Tracks, and Solos
        albums_links = self.browser. \
            find_elements_by_link_text('ALBUMS')
        inner_albums_links = self.browser. \
            find_elements_by_link_text('Albums')
        albums_links.extend(inner_albums_links)
        self.assertEqual(
            albums_links[0].get_attribute('href'),
            self.live_server_url + '/admin/albums/'
        )
        self.assertEqual(
            albums_links[1].get_attribute('href'),
            self.live_server_url + '/admin/albums/album/'
        )

        self.assertEqual(
            self.browser. \
                find_element_by_link_text('Tracks'). \
                get_attribute('href'),
                self.live_server_url + '/admin/albums/track/'
        )
        solos_links = self.browser. \
            find_elements_by_link_text('SOLOS')
        inner_solos_links = self.browser. \
            find_elements_by_link_text('Solos')
        solos_links.extend(inner_solos_links)
        self.assertEqual(
            solos_links[0].get_attribute('href'),
            self.live_server_url + '/admin/solos/'
        )
        self.assertEqual(
            solos_links[1].get_attribute('href'),
            self.live_server_url + '/admin/solos/solo/'
        )

        # He clicks on Albums and sees all of the Albums that
        # have been added so far
        albums_links[1].click()
        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Know What I Mean?').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/3/change/'
        )
        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Kind of Blue').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/2/change/'
        )
        self.assertEqual(
            self.browser.find_element_by_link_text(
                'My Favorite Things').get_attribute('href'),
            self.live_server_url + '/admin/albums/album/1/change/'
        )

        # Going back to the home page, he clicks the Tracks
        # link and sees the Tracks that have been added.
        # They're ordered first by Album, then by track
        # number.
        self.browser.find_element_by_css_selector(
            '#site-name a').click()
        self.browser.find_element_by_link_text('Tracks').click()

        track_rows = self.browser.find_elements_by_css_selector(
            '#result_list tr')
        self.assertEqual(track_rows[1].text,
                         'Kind of Blue Freddie Freeloader 2')
        self.assertEqual(track_rows[2].text,
                         'Kind of Blue Blue in Green 3')
        self.assertEqual(track_rows[3].text,
                         'Kind of Blue All Blues 4')
        self.assertEqual(track_rows[4].text,
                         'Know What I Mean? Waltz for Debby -')
        self.assertEqual(track_rows[5].text,
                         'My Favorite Things My Favorite Things -')

        # He adds a track to an album that already exists
        self.browser.find_element_by_link_text('ADD TRACK').click()

        track_form = self.browser.find_element_by_id('track_form')
        track_form.find_element_by_name('name').send_keys('So What')
        track_form.find_element_by_name('album'). \
            find_elements_by_tag_name('option')[1].click()

        track_form.find_element_by_name('track_number'). \
            send_keys('1')
        track_form.find_element_by_name('slug').send_keys('so-what')

        track_form.find_element_by_css_selector(
            '.submit-row input').click()
        self.assertEqual(
            self.browser.find_elements_by_css_selector(
                '#result_list tr')[1].text,
            'Kind of Blue So What 1'
        )

        # He adds another track, this time on an album that is not in
        # JMAD yet
        self.browser.find_element_by_link_text('ADD TRACK').click()
        track_form = self.browser.find_element_by_id('track_form')
        track_form.find_element_by_name('name'). \
            send_keys('My Funny Valentine')
        # After adding the basic Track info, he clicks on the plus
        # sign to add a new album.
        track_form.find_element_by_id('add_id_album').click()
        # The focus shifts to the newly opened window, where he sees
        # an Album form
        self.browser.switch_to.window(self.browser.window_handles[1])
        album_form = self.browser.find_element_by_id('album_form')
        album_form.find_element_by_name('name').send_keys('Cookin\'')
        album_form.find_element_by_name('artist'). \
            send_keys('Miles Davis Quintet')
        album_form.find_element_by_name('slug').send_keys('cookin')
        album_form.find_element_by_css_selector(
            '.submit-row input').click()

        # After adding the basic Track info, he clicks on the
        # plus sign to add a new album.
        # After creating the Album, he goes back to finish the Track
        self.browser.switch_to.window(self.browser.window_handles[0])
        track_form = self.browser.find_element_by_id('track_form')
        track_form.find_element_by_name('track_number'). \
            send_keys('1')
        track_form.find_element_by_name('slug'). \
            send_keys('my-funny-valentine')
        track_form.find_element_by_css_selector(
            '.submit-row input').click()
        self.assertEqual(
            self.browser.find_elements_by_css_selector(
                '#result_list tr'
            )[1].text,
            'Cookin\' My Funny Valentine 1'
        )

        # He goes back to the root of the admin site and clicks on
        # 'Solos'
        self.browser.find_element_by_css_selector(
            '#site-name a').click()
        self.browser.find_element_by_link_text('Solos').click()
        # He's sees Solos listed by Album, then Track, then start
        # time
        solo_rows = self.browser.find_elements_by_css_selector(
            '#result_list tr')
        self.assertEqual(solo_rows[1].text,
                         'All Blues Miles Davis 1:46-4:04')
        self.assertEqual(solo_rows[2].text,
                         'All Blues Cannonball Adderley 4:05-6:04')
        self.assertEqual(solo_rows[3].text.strip(),
                         'Waltz for Debby Cannonball Adderley -')
        self.assertEqual(solo_rows[4].text.strip(),
                         'My Favorite Things John Coltrane -')

        # He adds a Solo to a Track that already exists
        self.browser.find_element_by_link_text('ADD SOLO').click()
        solo_form = self.browser.find_element_by_id('solo_form')
        solo_form.find_element_by_name('track'). \
            find_elements_by_tag_name('option')[7].click()
        solo_form.find_element_by_name('artist'). \
            send_keys('McCoy Tyner')
        solo_form.find_element_by_name('instrument'). \
            send_keys('Piano')
        solo_form.find_element_by_name('start_time'). \
            send_keys('2:19')
        solo_form.find_element_by_name('end_time'). \
            send_keys('7:01')
        solo_form.find_element_by_name('slug'). \
            send_keys('mcoy-tyner')
        solo_form.find_element_by_css_selector(
            '.submit-row input').click()
        self.assertEqual(
            self.browser.find_elements_by_css_selector(
                '#result_list tr')[5].text,
            'My Favorite Things McCoy Tyner 2:19-7:01')

        # He then adds a Solo for which the Track and Album
        # do not yet exist
        self.browser.find_element_by_link_text('ADD SOLO').click()
        solo_form = self.browser.find_element_by_id('solo_form')

        # He adds a Track from the Solo page
        solo_form.find_element_by_id('add_id_track').click()
        self.browser.switch_to.window(self.browser.window_handles[1])
        track_form = self.browser.find_element_by_id('track_form')
        track_form.find_element_by_name('name'). \
            send_keys('In Walked Bud')

        # He adds an Album from the Track popup
        track_form.find_element_by_id('add_id_album').click()
        self.browser.switch_to.window(self.browser.window_handles[2])
        album_form = self.browser.find_element_by_id('album_form')
        album_form.find_element_by_name('name'). \
            send_keys('Misterioso')
        album_form.find_element_by_name('artist'). \
            send_keys('Thelonious Monk Quartet')
        album_form.find_element_by_name('slug'). \
            send_keys('misterioso')
        album_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He finishes up both parent objects, and saves the
        # Solo
        self.browser.switch_to.window(self.browser.window_handles[1])
        track_form = self.browser.find_element_by_id('track_form')
        track_form.find_element_by_name('track_number'). \
            send_keys('4')
        track_form.find_element_by_name('slug'). \
            send_keys('in-walked-bud')
        track_form.find_element_by_css_selector(
            '.submit-row input').click()

        self.browser.switch_to.window(self.browser.window_handles[0])
        solo_form = self.browser.find_element_by_id('solo_form')
        solo_form.find_element_by_name('artist'). \
            send_keys('Johnny Griffin')
        solo_form.find_element_by_name('instrument'). \
            send_keys('Tenor Saxophone')
        solo_form.find_element_by_name('start_time'). \
            send_keys('0:59')
        solo_form.find_element_by_name('end_time'). \
            send_keys('6:21')
        solo_form.find_element_by_name('slug'). \
            send_keys('johnny-griffin')
        solo_form.find_element_by_css_selector(
            '.submit-row input').click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector(
                '#result_list tr')[4].text,
            'In Walked Bud Johnny Griffin 0:59-6:21'
        )
