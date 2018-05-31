
"""
playlist.py

Description: Playing with iTunes Playlists.

Author: Mahesh Venkitachalam
Website: electronut.in
"""

import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np


# 多个播放列表中共同的乐曲音轨
def findCommonTracks(fileNames):
    """
    Find common tracks in given playlist files, and save them
    to common.txt.
    """
    # a list of sets of track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        plist = plistlib.readPlist(fileName)
        # get the tracks
        tracks = plist['Tracks']
        # iterate through tracks
        for trackId, track in tracks.items():
            try:
                # add name to set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass
        # add to list
        trackNameSets.append(trackNames)
    # get set of common tracks
    # intersection(*others)
    # set & other & ...
    # Return a new set with elements common to the set and all others.

    commonTracks = set.intersection(*trackNameSets)
    # write to file
    if len(commonTracks) > 0:
        f = open("common.txt", 'wb')
        # wb以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
        for val in commonTracks:
            s = "%s\n" % val
            f.write(s.encode("UTF-8"))
        f.close()
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")

# 评分和音轨时长，然后画一些图
def plotStats(fileName):
    """
    Plot some statistics by readin track information from playlist.
    """
    # read in playlist
    plist = plistlib.readPlist(fileName)
    # get the tracks
    tracks = plist['Tracks']
    # create lists of ratings and duration
    ratings = []
    durations = []
    # iterate through tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass

    # ensure valid data was collected
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s." % fileName)
        return

    # cross plot
    x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([0, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()


def findDuplicates(fileName):
    """
    Find duplicate tracks in given playlist.
    """
    print('Finding duplicate tracks in %s...' % fileName)
    # read in playlist
    plist = plistlib.readPlist(fileName)
    # 访问Tracks字典
    tracks = plist['Tracks']
    # 创建一个空的字典，用来保存重复的乐曲
    trackNames = {}
    # 开始用items()方法迭代Tracks字典
    for trackId, track in tracks.items():
        try:
            # 取得字典中每个音轨的名称和时长
            name = track['Name']
            duration = track['Total Time']
            # 检查当前乐曲的名称是否已在被构建的字典中?
            if name in trackNames:
                # 程序检查现有的音轨和新发现的音轨长度是否相同
                # 用//操作符，将每个音轨长度除以1000，由毫秒转换为秒，并四舍五入到最接近的秒，以进行检查
                if duration//1000 == trackNames[name][0]//1000:
                    # 如果确定这两个音轨长度相等，就取得与name关联的值，这是（duration，count）元组
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # 如果这是程序第一次遇到的音轨名称，就创建一个新条目，count为1
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass
    # 利用以下代码，提取重复的音轨
   
    # 创建一个空列表，保存重复乐曲
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save dups to file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")
    f = open("dups.txt", 'w')
    for val in dups:
        # 迭代遍历dups列表，写下重复的条目
        f.write("[%d] %s\n" % (val[0], val[1]))
    f.close()

# Gather our code in a main() function
def main():
    # create parser
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group .add_argument('--common', nargs = '*', dest='plFiles', required=False)
    group .add_argument('--stats', dest='plFile', required=False)
    group .add_argument('--dup', dest='plFileD', required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")

# main method
if __name__ == '__main__':
    main()
