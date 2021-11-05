# Extensibility

!!! caution
    **This documentation is a for legacy version of the purplship-server (up to 2021.7).**

    **Please visit [purplship.com/docs](https://purplship.com/docs) for the latest documentation.**

The obvious way to extend the purplship Server would be to download the source code and modify it directly.
After all it's an open-source platform. We advise against this as experience teaches us that once your store
diverges from the upstream purplship Server, it becomes hard to keep it updated.

Because of this we advice the use development of `Apps` that are external applications that talk to purplship Server
using its GraphQL and REST APIs additionally, they can subscribe to events using webhooks.


<figure>
  <img src="/images/purplship-apps-architecture.svg" height="300" />
</figure>
