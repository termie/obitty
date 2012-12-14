#!/usr/bin/env python
import json
import os
import re
import sys

import bs4


RE_ALPHA = re.compile(r'[\W]+')


def find_obit(html):
  soup = bs4.BeautifulSoup(html)
  ar = soup.select('#obitText span')
  if not ar:
    return None
  x = ar[0]

  c = x.children
  ob = {'img': None,
        'name': None,
        'text': []}
  first_img = True
  for y in c:
    tag = getattr(y, 'name', None)
    if tag == 'img' and first_img:
      ob['img'] = y['src']
      first_img = False
    if tag:
      continue
    if y.startswith('\r') or y.startswith('\n'):
      continue

    ob['text'].append(y)

  if ob['text']:
    ob['name'] = ob['text'][0].strip()
    ob['text'] = '\n'.join(ob['text'][1:])
    if ob['name'].startswith('Share your'):
      return None

    ob['stripped_name'] = RE_ALPHA.sub(' ', ob['name'])
    name_parts = ob['stripped_name'].split()
    ob['stripped_text'] = ob['text']
    for part in name_parts:
      ob['stripped_text'] = ob['stripped_text'].replace(part, 'XXX')

    return ob
  return None


def main_dir(target):
  files = os.listdir(target)
  obs = []
  for f in files:
    path = os.path.join(target, f)
    if f.startswith('obituary.aspx'):
      obs.append(find_obit(open(path).read()))
  obs = [x for x in obs if x]
  print json.dumps(obs, indent=4)


def main_list(stream):
  obs = []
  for path in stream:
    path = path.strip()
    obs.append(find_obit(open(path).read()))
  obs = [x for x in obs if x]
  print json.dumps(obs, indent=4)


if __name__ == '__main__':
  #cmd = sys.argv[1]
  #if len(sys.argv) < 3:
  #  cmd = 'dir'
  #  target = sys.argv[1]
  #else:
  #  target = sys.argv[2]

  #if cmd == 'dir':
  #  main_dir(target)
  #else:
  main_list(sys.stdin)
