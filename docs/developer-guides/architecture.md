# Architecture Overview

!!! caution
    **This documentation is a for legacy version of the purplship-server (up to 2021.7).**

    **Please visit [purplship.com/docs](https://purplship.com/docs) for the latest documentation.**

purplship has three main components:

1. The first component is the **purplship SDK** which unifies and standardize
   the communication to shipping carriers to one interface. It is designed
   to be extensible to allow integration of additional carrier support.

2. The second component is the **purplship server** which is the backend server
   that exposes a Shipping REST API, a GraphQL API and a Shipping Web App.
   The server is written in Python with Django. It maintains its state in a
   PostgresSQL database.

3. The third component is the **purplship Web App** which implements the user
   interface that operation members can be used to manage fulfilment processes.
   the app is a React application that runs in the browser and talks to the
   purplship server using the REST and Graph APIs.


<figure>
  <img src="/images/purplship-server-architecture.svg" />
</figure>
