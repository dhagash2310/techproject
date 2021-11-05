# Shipping

!!! caution
    **This documentation is a for legacy version of the purplship-server (up to 2021.7).**

    **Please visit [purplship.com/docs](https://purplship.com/docs) for the latest documentation.**

With purplship carrier connections, you can get live quotes and purchase shipping labels using the purplship API.
The web app uses purplship' API to streamline manual shipping processes.

The typical shipping process flow is

- Get live rates
- Choose a preferred rate
- Buy a label
- Print a label

## Get live rates

Getting shipping rates from the purplship Web App.

!!! info "Get shipping rates"

    - navigate to `> Shipments`
    - click on the `Create Label` button
    - Fill in the shipping details (shipper address, recipient address, parcel measurements...)
    - click on the `Fetch Rates` button when everything is ready

!!! quote ""
    <figure>
      <img src="/tutos/shipping-live-rates.gif" height="200" />
    </figure>


!!! note ""
    You can always go back to edit any shipment details or add options and refresh the rates.


## Buy a label

Buying a shipping label from the purplship Web App.

!!! info "Buying a shipping label"

    - from the `> Shipments / Create Label` panel
    - Select you prefered rate
    - Click the `Buy` button

!!! quote ""
    <figure>
      <img src="/tutos/shipping-label-purchase.gif" height="200" />
    </figure>


## Print a label

Printing a shipping label from the purplship Web App.

!!! info "Print a shipping label"

    - from the `> Shipments` panel
    - Click the `Print Label` action of your shipment

!!! quote ""
    <figure>
      <img src="/tutos/printing-label.gif" height="200" />
    </figure>


## International shipments

Shipping customs declaration from the purplship Web App.

!!! info "Shipping customs declaration"

    - from the `> Shipments / Create Label / Customs Info` panel

!!! quote ""
    <figure>
      <img src="/tutos/shipping-international-config.gif" height="200" />
    </figure>


## Void labels

Void shipping labels from the purplship Web App.

!!! info "Shipping customs declaration"

    - from the `> Shipments` panel
    - Click `Cancel Shipment` option on the shipment action dropdown

!!! quote ""
    <figure>
      <img src="/tutos/void-shipping-label.gif" height="200" />
    </figure>

