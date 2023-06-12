# Hire-A-Hacker

A CTFd compatible docker image for a web challenge. Scenario:

As malware infections are on the rise around the world, more and more hacker operations are becoming like businesses and offering their services to unscrupulous individuals who are willing to pay a cut to hurt their competitors. One such group has now launched an official "Hire-A-Hacker" website where customers can come to purchase these services. Maybe you can uncover some hidden information to help shut them down?

## Setup

Run the included build-docker.sh script to build and deploy the container in docker.

## Solution

The search field is vulnerable to SQL injection. Players are able to enumerate the vulnerability to discover the database engine being used and then find the "flag" table where the flag is hidden and leak it on the search page.

A payload like this works:

```xx' UNION SELECT 1,flag,1,1,1 FROM flag WHERE '%' = '```