import reddit
from cursebox import *
from cursebox.constants import *

# TODO display ssl status

with Cursebox() as cb:
    width, height = int(cb.width), int(cb.height)

    subreddits = reddit.getSubscribeSubreddits()
    posts = reddit.getPosts(subreddits[0].subreddit_name, height)
    content = None

    def login_screen():
        cb.clear()
        # todo define login form


    def show_subreddits():
        y = 0
        for subreddit in subreddits:
            bg = colors.black if y != scroll_vert[0] else colors.blue
            title = subreddit.name[:width / 3 - 3] + '...' if len(
                subreddit.title) > width / 3 else subreddit.title.ljust(width / 3)
            cb.put(0, y, title, fg=colors.white, bg=bg)
            y += 1


    # def get_subreddits():

    def show_posts():
        y = 0
        for post in posts:
            bg = colors.black if y != scroll_vert[1] else colors.blue
            title = post.title[:width / 3 - 3] + '...' if len(post.title) > width / 3 else post.title.ljust(width / 3)
            cb.put(width / 3, y, title, colors.white, bg)
            y += 1


    def show_content():
        cb.put(2 * width / 3, 0, content, colors.white, colors.black)


    def show_panes():
        show_subreddits()
        if curr_pane == 0:  # and index_changed:
            global posts
            posts = reddit.getPosts(subreddits[scroll_vert[0]], height)  # TODO add range parameters for paging
        elif curr_pane == 1:  # and index_changed:
            global content
            content = posts[scroll_vert[1]].getComments()
        show_posts()
        show_content()


    cb.clear()
    cb.put(width / 2 - 5, height / 2, "loading...", colors.white, colors.black)
    cb.refresh()

    scroll_vert = [0, 0, 0]
    curr_pane = 0

    while True:
        cb.clear()
        show_panes()
        # show_subreddits()
        # show_comments()
        cb.refresh()

        event = cb.poll_event()
        if event == EVENT_ESC:
            exit()
        elif event == EVENT_UP and scroll_vert[curr_pane] > 0:
            scroll_vert[curr_pane] -= 1
            # index_changed = True
        elif event == EVENT_DOWN and scroll_vert[curr_pane] < height:
            scroll_vert[curr_pane] += 1
            # index_changed = True
        elif event == EVENT_RIGHT and curr_pane < 3:
            curr_pane += 1
        elif event == EVENT_LEFT and curr_pane > 0:
            curr_pane -= 1
        elif event == 'r':
            pass
            # refresh_content()
