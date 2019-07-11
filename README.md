# Money stanfer system using SMS for county where internet is not always available 


## Agents
The first component of the system is the agents. They are responsible for sending and receiving money.
In order for the agent to use the system, the administrator must place it in the database first. To send or receive money, this system works with or without the Internet.
In this introduction we will see how we add agents to the system

## Add a proxy to the system

The first item is the number that the agent will use to send SMS messages to the server.

 This is very important if this number is not registered, the system will ignore any SMS from it.
Then the first name and last name.

 Then we have city and proxy address. This information will be used to help the customer find the location from which their money will be withdrawn. It can also be used to filter data by cities.

 Finally the password. This password will be used to connect to the system

  We now have an agent who can use the system. Using the same steps you can add more proxies.

  Remember that both the sending agent and the receiving agent need to be registered to be able to use the system.
  
 ## Conversions
 The second component of the system is conversions

The system helps us to send money through the agent (sender) to the agent (receiver). This money is for a particular customer (we have his phone number).

  We will see how any agent can send or receive via the system using SMS only.

  It is also possible to do the same if the agent has Internet.
      
