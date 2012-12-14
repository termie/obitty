#!/usr/bin/env python
import json
import os
import sys

import bs4


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
    return ob
  return None


def main(target):
  files = os.listdir(target)
  obs = []
  for f in files:
    path = os.path.join(target, f)
    if f.startswith('obituary.aspx'):
      obs.append(find_obit(open(path).read()))
  obs = [x for x in obs if x]
  print json.dumps(obs, indent=4)


if __name__ == '__main__':
  target = sys.argv[1]
  main(target)
