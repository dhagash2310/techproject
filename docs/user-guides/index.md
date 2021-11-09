# Getting Started

!!! caution
    **This documentation is a for legacy version of the purplship-server (up to 2021.7).**

    **Please visit [purplship.com/docs](https://next.purplship.com/docs) for the latest documentation.**

Once purplship is up and running, the first thing to do is to register your carrier accounts.

## Carrier connections

Adding carrier connection can be done from the purplship Web App.

!!! note "Connect a carrier account"

    - navigate to the `> Carriers` section
    - press on the `Connect Carrier`
    - select your carrier
    - fill in the connection / authorization API credentials
    - Submit

!!! quote ""
    <figure>
      <img src="/tutos/carrier-connection.gif" height="200" />
    </figure>

## Test vs Live Mode

purplship' first goal is to make shipping services integration and automation easy.

The `test mode` option here is suited for development. By checking the during your connection,
you are instructing purplship to connect to the carrier sandbox server.

!!! hint
    The `test mode` is great to experiment and test that your carrier integration is fully functional.

    Generally carriers will ignore all label purchased or any scheduled pickups in that mode.
    So you don't have to worry about any charges from carriers.

!!! note
    Leave it unchecked for `live mode` (in production)


From the purplship Web App, you can change the mode to visualize and operate the API in test mode
by enabling the `View test data` toggle.

!!! quote ""
    <figure>
      <img src="/tutos/view-test-data.gif" height="200" />
    </figure>
