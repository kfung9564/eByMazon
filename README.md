# eByMazon

## DJANGO NOTES
Register your completed model in admin.py
- **python manage.py makemigrations**
- **python manage.py migrate**

If you’re finished, run
- **python manage.py runserver**

If there’s no superuser, run the command
- **python manage.py createsuperuser**

Install these:
- **pip install django-tempus-dominus**
- **pip install django-phonenumber-field**
- **pip install phonenumbers**


Creating an “app” (this adds structure)
python manage.py startapp appname
Add it to the INSTALLED_APPS list in settings
Usually of the format
appname.apps.AppnameConfig
If not, check the apps.py file

create urls.py file
link said file to the urls.py file in the main app

Creating a “models” (this creates database tables)
Go to models.py
Django’s official website is a great and easy resource
https://docs.djangoproject.com/en/2.1/ref/models/

Register your completed model in admin.py
- **python manage.py makemigrations**
- **python manage.py migrate**

If you’re finished, run
- **python manage.py runserver**

If there’s no superuser, run the command
- **python manage.py createsuperuser**


## Tentative Checklist
User Applications:
- [x] submit to SUs the application to be an OU, which should include a unique id, the name, a valid credit card number, address, phone number.
- [x] Process applications and decide who can be OU and who should be denied. The initial password is the same as the id which the new OU is required to change the first time s/he logs in.

Buying/Selling Items
- [x] Submit the bid to buy an available item.
- [x] Sell the item s/he posted; for fixed price, the first one who posted the purchase intention should be chosen, otherwise the owner should provide a note justifying why the first one is not chosen; for price range, the one with the second highest bids should be chosen, otherwise the owner should provide a note of justification. 
- [ ] Submit purchasing intentions if no such item exists in the system, once someone post item(s) matching the keyword(s), the OU will receive notifications.
- [x] The tax of every sold item is automatically evaluated based on the address of the buying OU (have a dictionary keeping the tax rate for different states).

Item Applications
- [x] Submit to SUs the information (title, key words, price nature, at least one picture) of the item(s) s/he wants to sell. 
- [x] Process item information the OUs submitted intending to sell, some can be publicly available on the platform and some may be denied with justifications. An OU whose item is denied will be warned once.
- [x] Items removed from the system by SUs will be blacklisted from system. 

Complaints
- [x] File complaints to SUs against certain OUs whose item or payment has some problem or explain to the SU about any complaint received from others.
- [x] Process complaints: either removed or saved as justified ones after communicating with the OU who was complained.

Grading Users
- [x] Grade an OU after buying an item from him/her, 0 being the worst and 5 being the best. An OU who has submitted too many low ratings, three 0 or 1 ratings in a row, or high ratings, three 5 ratings in a row, will be warned by SU as possible reckless graders.
- [x] An OU will become a VIP OU if her/his rating is >= 4 (by at least 3 different OUs) or spent more than $500 and without warnings, any VIP will receive 5% discount when checking out. A VIP is moved to ordinary OU if his/her rating is below 4 automatically or received one warning.
- [ ] Send warnings to OUs who received two justified complaints or the average grade are lower than 2 with at least 3 different evaluators, should an OU receive two warnings this OU should be suspended from the system. A suspended OU will be notified when s/he logs in and can choose to appeal or resign. The appeal can be either approved or denied (then the user is removed).

User UI
- [x] See his/her own transaction history.
- [ ] When logging in, the system should have personalized recommendations to the OU based on his/her past search/purchase records, if no such information is available, the top 3 most popular items and OUs are displayed in the GUI.
- [ ] browse/search available items based on title, keywords, price (fixed or a range for bidding) and ratings;
- [x] Change his/her password, name, address, phone and credit card number, but not the id.
- [ ] An OU can maintain a friend list who will receive discount and friend-only messages, the OU is free to add/delete any OU from the list.

SU privilliages
- [x] Collect transaction statistics for a certain period (a day or a week) or a certain OU.  
- [ ] Maintain a taboo list with all inappropriate words, any OU’s keywords/name or items containing taboo words will be replaced by *** and the OU received one warning and required to change the word next time s/he logs in. [Don’t use real taboo words in your list, use mock ones instead to not offend anyone]
- [x] OUs removed from the system by SUs will be blocked based on the name for future re-application.
- [x] Have the right to remove any OU based on his/her judgment. A removed OU can log in to the system for the last time to clear matters, then the account is deleted afterwards.

Other constraints:
- [ ] GUI is required but not necessarily web-based.
- [ ] One creative feature worth 10% of the final project, such as speech interface, shipping/delivery plans or image content-based search, if your feature if very creative, your team will be rewarded by an up to 10% bonus.
