#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

def regularize_image(s):
    '''
    >>> regularize_image('卷上(<img src=\"gif/9/9FB9.gif\" width=\"20\">) 齿')
    '卷上(龹) 齿'
    '''
    return re.sub(r'<img src="[^"]+\/([0-9A-F]+).gif" width="20">', lambda m: chr(int(m.group(1), base=16)), s)

def regularize_data(s):
    '''
    >>> regularize_data('旦(亶)')
    '旦'
    >>> regularize_data('卷上(龹)')
    '卷'
    >>> regularize_data('孌音(䜌)')
    '孌'
    >>> regularize_data('莹音')
    '莹'
    >>> regularize_data('丰(串义)')
    '串'
    '''
    s = re.sub(r'^(.)[上下音义]?(\(.\))?$', r'\1', s)
    return re.sub(r'^.\((.)[上下音义]\)$', r'\1', s)

# Override malformed data
override_table = \
    { '兿': '䒑云'
    , '労': '小力'
    , '勬': '卷力'
    , '厨': '厂寸'
    , '唢': '口锁'
    , '営': '小吕'
    , '喾': '小告'
    , '囪': '囗乂'
    , '坚': '丨土'
    , '峃': '小山'
    , '憂': '百夂'
    , '憩': '舌心'
    , '憲': '宀心'
    , '懐': '忄衣'
    , '戞': '一戈'
    , '摂': '扌耳'
    , '琐': '王锁'
    , '锁': '钅锁'
    , '𫦁': '锁刂'
    , '𫼶': '扌锁'
    , '𭾪': '四衣'
    , '𮍦': '臼衣'
    , '𮕻': '衣日'
    , '𮝾': '厂衣'
    }

def regularize_liangfen(s, ch):
    if ch in override_table:
        return override_table[ch]

    s = regularize_image(s)
    liangfen_l, liangfen_r = s.split(' ')
    
    liangfen_l = regularize_data(liangfen_l)
    liangfen_r = regularize_data(liangfen_r)

    assert len(liangfen_l) == 1 and len(liangfen_r) in (0, 1)
    return liangfen_l, liangfen_r

def main():
    with open('zisea-20200724.jsonl') as f, open('liangfen.txt', 'w') as g:
        for line in f:
            obj = json.loads(line)

            codepoint = obj['cp']
            ch = chr(int(codepoint, base=16))

            liangfen = obj['lfzy']
            liangfen_l, liangfen_r = regularize_liangfen(liangfen, ch)

            print(ch, liangfen_l + liangfen_r, file=g)

if __name__ == '__main__':
    main()
