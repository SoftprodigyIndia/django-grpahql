**Dynamo db using python**

Create table: done using **create\_table .**

Ex

Step-1. Make.py file
Step-2. Import boto

Step-3. you must provide : table name, primary key(key schema,attribute definitions, throughput provision(ReadCapacityUnits,WriteCapacityUnits)

Step-4. run file by : python filename.py

Load Sample Data(just like seeder in python django or adding data to table through external json file): done using **put\_item**

**Ex**

Step-1. py file
Step-2. Import boto

Step-3. you must use put\_item to add data in a specific table

Step-4. run file by : python filename.py

Create/Insert Item : done using **put\_item**

**Ex :** table = dynamodb.Table(&#39;Movies&#39;)

response = table.put\_item(

Item={

&#39;year&#39;: year,

&#39;title&#39;: title,
}
)

Read Item : done using **get\_item (just like a get() in django orm)**

In this we need to specify a key to filter
Ex:

table = dynamodb.Table(&#39;Movies&#39;)
try:

response = table.get\_item(Key={&#39;year&#39;: year, &#39;title&#39;: title})
except ClientError as e:
print(e.response[&#39;Error&#39;][&#39;Message&#39;])

else:

return response[&#39;Item&#39;]

Update Item : done using **update\_item (just like a update() in django orm)**

In this we need to specify a key to filter

Ex: table = dynamodb.Table(&#39;Movies&#39;)

response = table.update\_item(

Key={

&#39;year&#39;: year,

&#39;title&#39;: title

},

UpdateExpression=&quot;set info.rating=:r, info.plot=:p, info.actors=:a&quot;,

ExpressionAttributeValues={

&#39;:r&#39;: Decimal(rating),

&#39;:p&#39;: plot,

&#39;:a&#39;: actors

},

ReturnValues=&quot;UPDATED\_NEW&quot;

)

Update Item Conditionally : done using **update\_item (just like a update() in django orm) but with a condition expression**

**If the condition evaluates to true, the update succeeds; otherwise, the update is not performed.**

**Ex:**

try:

response = table.update\_item(

Key={

&#39;year&#39;: year,

&#39;title&#39;: title

},

UpdateExpression=&quot;remove info.actors[0]&quot;,

ConditionExpression=&quot;size(info.actors) \&gt; :num&quot;,

ExpressionAttributeValues={&#39;:num&#39;: actor\_count},

ReturnValues=&quot;UPDATED\_NEW&quot;

)

except ClientError as e:

if e.response[&#39;Error&#39;][&#39;Code&#39;] == &quot;ConditionalCheckFailedException&quot;:

print(e.response[&#39;Error&#39;][&#39;Message&#39;])

else:

raise

else:

return response

Delete Item : done using **delete\_item (just like a delete() in django orm)**

In this we need to specify a key to filter

Ex:

try:

response = table.delete\_item(

Key={

&#39;year&#39;: year,

&#39;title&#39;: title

},

ConditionExpression=&quot;info.rating \&lt;= :val&quot;,

ExpressionAttributeValues={

&quot;:val&quot;: Decimal(rating)

}

)

except ClientError as e:

if e.response[&#39;Error&#39;][&#39;Code&#39;] == &quot;ConditionalCheckFailedException&quot;:

print(e.response[&#39;Error&#39;][&#39;Message&#39;])

else:

raise

else:

return response

Increment an Atomic Counter:

DynamoDB supports atomic counters, which use the update\_item method to increment or decrement the value of an existing attribute without interfering with other write requests. (All write requests are applied in the order in which they are received.)

Query data: : done using **query (just like a filter() in django orm)**

In this we need to specify a key to filter

Ex:

table = dynamodb.Table(&#39;Movies&#39;)

response = table.query(

KeyConditionExpression=Key(&#39;year&#39;).eq(year)

)

**NOTE:The Boto 3 SDK constructs a ConditionExpression for you when you use the Key and Attr functions imported from boto3.dynamodb.conditions. You can also specify a ConditionExpression as a string.**

**NOTE- if you want only some fields to be returned in response(just like we use values in django orm):
 Then we can use **** ProjectionExpression **** for that:**

**Ex:**
table = dynamodb.Table(&#39;Movies&#39;)

response = table.query(

ProjectionExpression=&quot;#yr, title, info.genres, info.actors[0]&quot;,

ExpressionAttributeNames={&quot;#yr&quot;: &quot;year&quot;},

KeyConditionExpression=

Key(&#39;year&#39;).eq(year) &amp; Key(&#39;title&#39;).between(title\_range[0], title\_range[1])

)

return response[&#39;Items&#39;]

Scan data: : done using **scan (just like a all() in django orm)**

**The scan method reads every item in the entire table and returns all the data in the table. You can provide an optional**  **filter\_expression**  **so that only the items matching your criteria are returned. However, the filter is applied only after the entire table has been scanned.**

In this we can specify a **filter\_expression** to filter.(optional)

Ex:

table = dynamodb.Table(&#39;Movies&#39;)

response = table.scan(

&#39;FilterExpression&#39;: Key(&#39;year&#39;).between(\*year\_range),

&#39;ProjectionExpression&#39;: &quot;#yr, title, info.rating&quot;,

&#39;ExpressionAttributeNames&#39;: {&quot;#yr&quot;: &quot;year&quot;}

)

Delete a table : done using **delete**

**Ex:**

table = dynamodb.Table(&#39;Movies&#39;)

table.delete()

.
