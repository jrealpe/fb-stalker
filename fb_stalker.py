import argparse
import requests
from fb_parcer import *
from tabulate import tabulate

URL = 'https://m.facebook.com/'

def login(session, email, password):

    '''
    Attempt to login to Facebook. Gets user ID, xs token and
    fb_dtsg token. All 3 are required to make requests to
    Facebook endpoints as a logged in user. Returns False if
    login Gets
    '''

    # Navigate to Facebook's homepage to load Facebook's cookies.
    response = session.get(URL)

    # Attempt to login to Facebook
    response = session.post(URL + 'login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)

    # If c_user cookie is present, login was successful
    if 'c_user' in response.cookies:

        # Get c_user
        user_id = response.cookies['c_user']

        # Get xs
        xs = response.cookies['xs']


        # Make a request to homepage
        response = session.get(URL + 'home.php')

        # Parser response
        parse_page = get_bs(response.text)

        # Get fb_dtsg token
        fb_dtsg = get_fb_dtsg_token(parse_page)

        # Get logout link
        fb_logout = get_fb_logout(parse_page)

        return True, fb_logout
    else:
        return False, ''

def stalker(session):

    # To get started
    next = 'friends/center/friends/'
    l_friends = []

    while next:
        # Navigate to Facebook's friends.
        response = session.get(URL + next)
        parse_page = get_bs(response.text)

        # Get friends's list (10)
        friends = get_fb_friends(parse_page)

        for friend in friends:
            url = URL + friend[1]
            res = session.get(url)
            friend = list(friend)
            friend.append(str(res.status_code))
            friend.append(url)
            l_friends.append(tuple(friend))

        # Get next page
        next = get_fb_friends_next(parse_page)

    # Show status
    print(tabulate(l_friends, headers=['NOMBRE','ID','ESTADO','URL'], tablefmt="fancy_grid"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Login to Facebook')
    parser.add_argument('email', help='Email address')
    parser.add_argument('password', help='Login password')

    args = parser.parse_args()

    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
    })

    print_title()
    success, fb_logout = login(session, args.email, args.password)

    if success:
        print('Login Success')
        stalker(session)
        session.get(URL + fb_logout)
        print('Logout Success')
    else:
        print('Login Failed')
