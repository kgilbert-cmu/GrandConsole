import facebook
import requests ## after the initial GraphAPI call, pagination gives a GET'able URL
import logging
import sys

from collections import Counter

import local_config


def setup():
	logging.basicConfig(level = logging.INFO)


def main():
	auth = local_config.access_token
	groupID = local_config.ID
	
	graph = facebook.GraphAPI(auth)
	try:
		group = graph.get_object(groupID)
	except facebook.GraphAPIError:
		logging.exception(f"GrandConsole could not access specified group `{groupID}`. Check your permissions and verify OAth token.")
		sys.exit(1)
	
	queue = graph.get_connections(group['id'], "feed")
	posts = []
	comments = []
	likes = []
	most_liked_post = {}
	nlikes = 0
	most_commented_post = {}
	ncomments = 0
	likes_and_comments = {}
	both = 0
	while len(queue['data']) > 0: # break when there's no more pages...
		logging.info(f"Search result returned {len(queue['data'])} more results")
		for item in queue['data']:
			logging.debug(f"Inspecting next item {item['id']} from {item['from']['name']}")
			p = { 'name' : item['from']['name'],
			      'date' : item['created_time'] }
			posts.append(p)
			if 'likes' in item:
				likes.extend(item['likes']['data'])
				
				if len(item['likes']['data']) > nlikes:
					most_liked_post = item
					nlikes = len(item['likes']['data'])
				if 'comments' in item:
					subcomment_likes = [c['like_count'] for c in item['comments']['data']]
					if len(item['likes']['data']) + sum(subcomment_likes) > both:
						likes_and_comments = item
						both = len(item['likes']['data']) + sum(subcomment_likes)
			if 'comments' in item:
				comments.extend(item['comments']['data'])
				if len(item['comments']['data']) > ncomments:
					most_commented_post = item
					ncomments = len(item['comments']['data'])
			
		if 'paging' in queue and 'next' in queue['paging']:
			# replace queue with new page of search results
			queue = requests.get(queue['paging']['next']).json()
		else:
			queue = { 'data' : [] } # clear queue and exit
	
	logging.info(f"Most liked post: {most_liked_post['actions'][0]['link']}")
	logging.info(f"Most commented post: {most_commented_post['actions'][0]['link']}")
	logging.info(f"Most popular post: {likes_and_comments['actions'][0]['link']}")
	logging.info(f"Total number of likes: {len(likes)}")
	logging.info(f"Total number of comments: {len(comments)}")
	logging.info(f"Total number of posts: {len(posts)}")
	
	row_format = "{:<30}{:>3}"
	
	likeCounts = {}
	for l in likes:
		if l['name'] in likeCounts:
			likeCounts[l['name']] += 1
		else:
			likeCounts[l['name']] = 1
	likeCounter = Counter(likeCounts).most_common(10)
	logging.info("Most likes:")
	for u, n in likeCounter:
		print(row_format.format(u, n))
	print("")
	
	commentCounts = {}
	for c in comments:
		if c['from']['name'] in commentCounts:
			commentCounts[c['from']['name']] += 1
		else:
			commentCounts[c['from']['name']] = 1
	commentCounter = Counter(commentCounts).most_common(10)
	logging.info("Most comments:")
	for u, n in commentCounter:
		print(row_format.format(u, n))
	print("")

	postCounts = {}
	for p in posts:
		if p['name'] in postCounts:
			postCounts[p['name']] += 1
		else:
			postCounts[p['name']] = 1
	postCounter = Counter(postCounts).most_common(10)
	logging.info("Most posts:")
	for u, n in postCounter:
		print(row_format.format(u, n))
	print("")	

if __name__ == "__main__":
	setup()
	main()

