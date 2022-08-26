<div align="center">
<!-- Title: -->
<h1>House rent</h1>
<!-- Description: -->
<p>This is a notification bot for rent a house.</p>
</div>
<div>
In order to rent a house, maybe you needed to constantly check the divar application to see if there is any new house available.
So this bot notify you when a new house is available that was advertised according to your criteria.
<div>
<!-- Table of Contents: -->
<h2>Table of Contents</h2>
<ul>
<li><a href="#installation">Installation</a></li>
<li><a href="#usage">Usage</a></li>

<div>
<!-- Installation: -->
<h2 id="installation">Installation</h2>
<p>
<!-- Install the package: -->
<code>pip install -r requirements.txt</code>
</p>
</div>
 
<div>
<!-- Usage: -->
<h2 id="usage">Usage</h2>
<p>

```python
# Set token, channel_id
token = "YOUR_TOKEN"
chanel_id = "YOUR_CHANEL_ID"

# Create a notification bot
bot = BotDivar(token=token, channel_id=chanel_id)
bot.start_polling()
```
</br>
Note: Please call /help to see the available commands in the bot.
</p>
</div>