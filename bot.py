import requests as r,json,os,time;from datetime import datetime as d
h,p=os.environ['BSKY_HANDLE'],os.environ['BSKY_PASS']
i=r.get('https://api.ipify.org').text
u=f"https://chaturbate.com/api/public/affiliates/onlinerooms/?wm=T2CSW&client_ip={i}&format=json&limit=50&gender=f&hd=true"
s=r.get(u).json()['results']
posted=json.load(open('posted.json'))if os.path.exists('posted.json')else{}
n=time.time()
c=[x for x in s if x['username']not in posted or n-posted.get(x['username'],0)>86400]
if not c:exit()
c.sort(key=lambda x:-x.get('num_users',0));p=c[0]
t=' '.join(f'#{tag}'for tag in p['tags']+['nsfw','nsfwsky'])
txt=f"🔥LIVE RIGHT NOW!🔥 {p['username']} is teasing {p['room_subject']}! 👉{p['chat_room_url']} {t} 😈 Thousands watching — join the party!"
posted[p['username']]=n
json.dump(posted,open('posted.json','w'))
j=r.post('https://bsky.social/xrpc/com.atproto.server.createSession',json={'identifier':h,'password':p}).json()['accessJwt']
r.post('https://bsky.social/xrpc/com.atproto.repo.createRecord',headers={'Authorization':f'Bearer {j}'},json={'repo':h,'collection':'app.bsky.feed.post','record':{'$type':'app.bsky.feed.post','text':txt,'createdAt':d.utcnow().isoformat()+'Z'}})
