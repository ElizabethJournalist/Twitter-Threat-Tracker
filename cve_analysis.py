import csv
import operator
from collections import Counter

tweets_file_name = 'CVE_tweets.csv'
sorted_file_name = 'CVE_sorted.csv'

# Sort tweets
sample = open(tweets_file_name, 'r')
csv1 = csv.reader(sample, delimiter=',')
sort = sorted(csv1, key=operator.itemgetter(1))

for eachline in sort:
    with open(sorted_file_name, 'a', encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(eachline)
##

# ##  Opens and reads CVE_tweets.csv file.  The for loop allow you to select column by name
# with open(tweets_file_name) as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['cve'], row['text'])  # first test printed out  columns cve and text
# #  #      print(row['user'], row['followers_count'])

##########################################################################################################


cve_count = {}


with open(tweets_file_name) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cve = row['cve']
        if cve in cve_count:
            cve_count[cve] += 1
        else:
            cve_count[cve] = 1


#print(cve_count)

### Print top CVEs
print()
print("=== TOP CVES ===\n")
d = Counter(cve_count)
top_cves = d.most_common(10)

print(" {:<40}|{:^13}|  {:<60}|".format("CVE", "Count", "Link"))
print("="*119)
for cve, count in top_cves:
    print(" {:<40}|{:^13}|  {:<60}|".format(cve, str(count), "https://nvd.nist.gov/vuln/detail/" + cve))



##############################################################################################################




#
# print("==  USER + FOLLOWERS 2 version ===")
#
# combined = {}
#
# with open(tweets_file_name) as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         user = row['user']
#         followers = row['followers_count']
#         #reader[user] = reader[user].map(str) + reader["followers"]
#         #pd.merge(user, followers, left_on='user', right_on='followers')
#         print("User: " + user + " " + "-- Followers: " + followers)



####################################################################   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#print("== Users and followers List===")

user_count = {}
follower_count = {}

with open(tweets_file_name) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        followers = row['followers_count']
        user = row['user']
        #user = user + "_followers_" + followers
        sep = '_'
        #rest = user.split(sep, 1)[0]

        if user in user_count:
            user_count[user] += 1
        else:
            user_count[user] = 1
            follower_count[user] = followers

#print(user_count)

print("\n\n")
### Print top Users
print("=== TOP 10 USERS and followers  ===\n")
d = Counter(user_count)
top_users = d.most_common(10)

#for key, value in dictionary:
print(" {:<40}|{:^13}|{:^10}|  {:<60}|".format("User Name", "Followers", "# Tweets", "Link"))
print("="*130)
for user, count in top_users:
    print(" {:<40}|{:^13}|{:^10}|  {:<60}|".format(user, follower_count[user], str(count), "https://twitter.com/" + user))
    #print('User name: ' + user + " (Followers: " + follower_count[user] + ")" + " -- Tweeted: " + str(count)  + " " +  "times" + "--Link: https://twitter.com/" + user)
