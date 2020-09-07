#Start by making the OpenOPC library available to your application. This imports the OpenOPC.py module file located in the lib/site-packages/ directory.
import OpenOPC

#DCOM mode is used to talk directly to OPC servers without the need for the OpenOPC Gateway Service. This mode is only available to Windows clients.
#opc = OpenOPC.client()
#In Open mode a connection is made to the OpenOPC Gateway Service running on the specified node. This mode is available to both Windows and non-Windows clients
IP ='192.168.7.146'
opc = OpenOPC.open_client(IP)

#opc.servers()
#['Matrikon.OPC.Simulation.1', 'Kepware.KEPServerEX.V4']
#If the OPC server is running on a different node, you can include the optional host parameter
OPC_Name='Kepware.KEPServerEX.V6'
opc.connect( OPC_Name, IP)

#Read the specified OPC item. The function returns a (value, quality, timestamp) tuple. If the call fails, the quality will be set to 'Error'.

Channel='Channel1.'
Device='Device1.'
Tag='Temp'
Data=opc.read(Channel+Device+Tag)

print(Data)
'''
value, quality, time = opc.read('Random.Int4')
#When using the special short form of the function, only the value portion is returned. If any problems are encountered, value will be set to None.
value = opc['Random.Int4']
#Reading multiple items
# values may be read with a single call by passing a list of item names. Whenever a list is provided as input, the read function returns back a list of (name, value, quality, time) tuples.
opc.read( ['Random.Int2', 'Random.Real4', 'Random.String'] )
[('Random.Int2', 28145, 'Good', '06/24/07 17:44:43'), ('Random.Real4', 19025.2324, 'Good', '06/24/07 17:44:43'), ('Random.String', 'your', 'Good', '06/24/07 17:44:43')]

#There is a special version of read function called iread (Iterative Read). iread returns a Python generator which can be used to iterate through the returned results, item by item.
for name, value, quality, time in opc.iread( ['Random.Int2', 'Random.Int4'] ):
   print name, value
#Reading items using OPC Groups
#For best performance it is often necessary to place the items into a named group, then repeatedly request the group's values be updated. Including both the item list along with a group name will cause a new group to be defined and an initial read to be preformed.
tags = ['Random.String', 'Random.Int4', 'Random.Real4']

opc.read(tags, group='test')
[('Random.String', 'options', 'Good', '06/24/07 23:38:24'), ('Random.Int4', 31101, 'Good', '06/24/07 23:38:24'), ('Random.Real4', 19933.958984375, 'Good', '06/24/07 23:38:24')]
#Once the group has been defined, you can re-read the items in the group by supplying only the group name. You can repeat this call as often as necessary.
opc.read(group='test')
[('Random.String', 'clients', 'Good', '06/24/07 23:38:30'), ('Random.Int4', 26308, 'Good', '06/24/07 23:38:30'), ('Random.Real4', 13846.63671875, 'Good', '06/24/07 23:38:30')]
#When you are done using the group, be sure to remove it. This will free up any allocated resources. If the removal was successful True will be returned, otherwise False.
opc.remove('test')

#Writing a single item
#Writing a single item can be accomplished by submitting a (name, value) tuple to the write function. If the write was successful True is returned, or False on failure.
opc.write( ('Triangle Waves.Real8', 100.0) )
#Success'
#You can also use the short form...
opc['Triangle Waves.Real8'] = 100.0
#Writing multiple items
#To write multiple items at once, submit a list of (name, value) tuples. The function returns a list of (name, status) tuples letting you know for each item name if the write attempt was successful or not.
opc.write( [('Triangle Waves.Real4', 10.0), ('Random.String', 20.0)] )
[('Triangle Waves.Real4', 'Success'), ('Random.String', 'Error')]
#The iwrite function returns a generator designed for iterating through the return statuses item by item...
for item, status in opc.iwrite( [('Triangle Waves.Real4', 10.0), ('Random.String', 20.0)] ):
   print item, status
#Getting error message strings
#Including the optional include_error=True parameter will cause many of the OpenOPC functions to append a descriptive error message to the end of each item tuple. In the case of the write function, it will return (name, status, error) tuples.
opc.write( [('Triangle Waves.Real4', 10.0), ('Random.Int4', 20.0)], include_error=True)
[('Triangle Waves.Real4', 'Success', 'The operation completed successfully'), ('Random.Int4', 'Error', "The item's access rights do not allow the operation")]
#Retrieving item properties
#Requesting properties for a single item returns a list of (id, description, value) tuples. Each tuple in the list represents a single property.
opc.properties('Random.Int4')
[(1, 'Item Canonical DataType', 'VT_I4'), (2, 'Item Value', 491), (3, 'Item Quality', 'Good'), (4, 'Item Timestamp', '06/25/07 02:24:44'), (5, 'Item Access Rights', 'Read'), (6, 'Server Scan Rate', 100.0), (7, 'Item EU Type', 0), (8, 'Item EUInfo', None), (101, 'Item Description', 'Random value.')]
#If a list of items is submitted, the item name will be appended to the beginning of each tuple to produce a list of (name, id, description, value) tuples.
opc.properties( ['Random.Int2', 'Random.Int4', 'Random.String'] )
[('Random.Int2', 1, 'Item Canonical DataType', 'VT_I2'), ('Random.Int2', 2, 'Item Value', 4827), ('Random.Int2', 3, 'Item Quality', 'Good'), ('Random.Int2', 4, 'Item Timestamp', '06/25/07 02:35:28'), ('Random.Int2', 5, 'Item Access Rights', 'Read'), ('Random.Int2', 6, 'Server Scan Rate', 100.0), ('Random.Int2', 7, 'Item EU Type', 0), ('Random.Int2', 8, 'Item EUInfo', None), ('Random.Int2', 101, 'Item Description', 'Random value.'), ('Random.Int4', 1, 'Item Canonical DataType', 'VT_I4'), ('Random.Int4', 2, 'Item Value', 14604), ('Random.Int4', 3, 'Item Quality', 'Good'), ('Random.Int4', 4, 'Item Timestamp', '06/25/07 02:35:28'), ('Random.Int4', 5, 'Item Access Rights', 'Read'), ('Random.Int4', 6, 'Server Scan Rate', 100.0), ('Random.Int4', 7, 'Item EU Type', 0), ('Random.Int4', 8, 'Item EUInfo', None), ('Random.Int4', 101, 'Item Description', 'Random value.'), ('Random.String', 1, 'Item Canonical DataType', 'VT_BSTR'), ('Random.String', 2, 'Item Value', 'profit...'), ('Random.String', 3, 'Item Quality', 'Good'), ('Random.String', 4, 'Item Timestamp', '06/25/07 02:35:28'), ('Random.String', 5, 'Item Access Rights', 'Read'), ('Random.String', 6, 'Server Scan Rate', 100.0), ('Random.String', 7, 'Item EU Type', 0), ('Random.String', 8, 'Item EUInfo', None), ('Random.String', 101, 'Item Description', 'Random value.')]
#The optional id parameter can be used to limit the returned value to that of a single property...
opc.properties('Random.Int4', id=1)
#'VT_I4'
#Like other OpenOPC function calls, providing a list of items causes the item names to be included in the output...
opc.properties( ['Random.Int2', 'Random.Int4', 'Random.String'], id=1)
[('Random.Int2', 'VT_I2'), ('Random.Int4', 'VT_I4'), ('Random.String', 'VT_BSTR')]
#The id parameter can also be used to specify a list of ids...
opc.properties('Random.Int4', id=(1,2,5))
[(1, 'VT_I4'), (2, 1869), (5, 'Read')]
#Getting a list of available items
#List nodes at the root of the tree...
opc.list()
['Simulation Items', 'Configured Aliases']
#List nodes under the Simulation Items branch...
opc.list('Simulation Items')
['Bucket Brigade', 'Random', 'Read Error', 'Saw-toothed Waves', 'Square Waves', 'Triangle Waves', 'Write Error', 'Write Only']
#Use the "." character as a seperator between branch names...
opc.list('Simulation Items.Random')
['Random.ArrayOfReal8', 'Random.ArrayOfString', 'Random.Boolean', 'Random.Int1', 'Random.Int2', 'Random.Int4', 'Random.Money', 'Random.Qualities', 'Random.Real4', 'Random.Real8', 'Random.String', 'Random.Time', 'Random.UInt1', 'Random.UInt2', 'Random.UInt4']
#You can use Unix and DOS style wildcards...
opc.list('Simulation Items.Random.*Real*')
['Random.ArrayOfReal8', 'Random.Real4', 'Random.Real8']
#If recursive=True is included, you can include wildcards in multiple parts of the path. The function will go thru the entire tree returning all children (leaf nodes) which match.
opc.list('Sim*.R*.Real*', recursive=True)
['Random.Real4', 'Random.Real8', 'Read Error.Real4', 'Read Error.Real8']
#Including the optional flat=True parameter flattens out the entire tree into leaf nodes, freeing you from needing to be concerned with the hierarchical structure. (Note that this function is not implemented consistantly in many OPC servers)
opc.list('*.Real4', flat=True)
['Bucket Brigade.Real4', 'Random.Real4', 'Read Error.Real4', 'Saw-toothed Waves.Real4', 'Square Waves.Real4', 'Triangle Waves.Real4', 'Write Error.Real4', 'Write Only.Real4']
#You can also submit a list of item search patterns. The returned results will be a union of the matching nodes.
opc.list(('Simulation Items.Random.*Int*', 'Simulation Items.Random.Real*'))
['Random.Int1', 'Random.Int2', 'Random.Int4', 'Random.UInt1', 'Random.UInt2', 'Random.UInt4', 'Random.Real4', 'Random.Real8']
#Retrieving OPC server information
opc.info()
[('Host', 'localhost'), ('Server', 'Matrikon.OPC.Simulation'), ('State', 'Running'), ('Version', '1.1 (Build 307)'), ('Browser', 'Hierarchical'), ('Start Time', '06/24/07 13:50:54'), ('Current Time', '06/24/07 18:30:11'), ('Vendor', 'Matrikon Consulting Inc (780) 448-1010 http://www.matrikon.com')]
#Combine functions together
#The output from many of the OpenOPC functions can be used as input to other OpenOPC functions. This allows you to employ a functional programming style which is concise and doesn't require the use of temporary variables.

#Read the values of all Random integer items...
opc.read(opc.list('Simulation Items.Random.*Int*'))
[('Random.Int1', 99, 'Good', '06/24/07 22:44:28'), ('Random.Int2', 26299, 'Good', '06/24/07 22:44:28'), ('Random.Int4', 17035, 'Good', '06/24/07 22:44:28'), ('Random.UInt1', 77, 'Good', '06/24/07 22:44:28'), ('Random.UInt2', 28703, 'Good', '06/24/07 22:44:28'), ('Random.UInt4', 23811.0, 'Good', '06/24/07 22:44:28')]
#Read property #1 (data type) of all Real4 items...
opc.properties(opc.list('*.Real4', flat=True), id=1)
[('Bucket Brigade.Real4', 'VT_R4'), ('Random.Real4', 'VT_R4'), ('Read Error.Real4', 'VT_R4'), ('Saw-toothed Waves.Real4', 'VT_R4'), ('Square Waves.Real4', 'VT_R4'), ('Triangle Waves.Real4', 'VT_R4'), ('Write Error.Real4', 'VT_R4'), ('Write Only.Real4', 'VT_R4')]
#Read the value of all Triangle Wave integers and then write the values back out to the OPC server. (A better example would be to do this between two different OPC servers!)
opc.write(opc.read(opc.list('Simulation Items.Triangle Waves.*Int*')))
[('Triangle Waves.Int1', 'Success'), ('Triangle Waves.Int2', 'Success'), ('Triangle Waves.Int4', 'Success'), ('Triangle Waves.UInt1', 'Success'), ('Triangle Waves.UInt2', 'Success'), ('Triangle Waves.UInt4', 'Success')]
#The short form of the read and write functions are useful for building easy to read calculations...
opc['Square Waves.Real4'] = ( opc['Random.Int4'] * opc['Random.Real4'] ) / 100.0
#Remove all named groups which were created with the read function...
opc.remove(opc.groups())
#Disconnecting from the OPC server
opc.close()
'''