/* tslint:disable */
/* eslint-disable */
/**
 * Karrio API
 *  ## API Reference  Karrio is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services.  The Karrio API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.  The Karrio API differs for every account as we release new versions. These docs are customized to your version of the API.   ## Versioning  When backwards-incompatible changes are made to the API, a new, dated version is released. The current version is `2022.3.2`.  Read our API changelog and to learn more about backwards compatibility.  As a precaution, use API versioning to check a new API version before committing to an upgrade.   ## Pagination  All top-level API resources have support for bulk fetches via \"list\" API methods. For instance, you can list addresses, list shipments, and list trackers. These list API methods share a common structure, taking at least these two parameters: limit, and offset.  Karrio utilizes offset-based pagination via the offset and limit parameters. Both parameters take a number as value (see below) and return objects in reverse chronological order. The offset parameter returns objects listed after an index. The limit parameter take a limit on the number of objects to be returned from 1 to 100.   ```json {     \"next\": \"/v1/shipments?limit=25&offset=25\",     \"previous\": \"/v1/shipments?limit=25&offset=25\",     \"results\": [     ] } ```  ## Environments  The Karrio API offer the possibility to create and retrieve certain objects in `test_mode`. In development, it is therefore possible to add carrier connections, get live rates, buy labels, create trackers and schedule pickups in `test_mode`.  
 *
 * The version of the OpenAPI document: 2022.3.2
 * Contact: 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import {
    Address,
    AddressFromJSON,
    AddressFromJSONTyped,
    AddressToJSON,
} from './Address';
import {
    Charge,
    ChargeFromJSON,
    ChargeFromJSONTyped,
    ChargeToJSON,
} from './Charge';
import {
    Parcel,
    ParcelFromJSON,
    ParcelFromJSONTyped,
    ParcelToJSON,
} from './Parcel';

/**
 * 
 * @export
 * @interface Pickup
 */
export interface Pickup {
    /**
     * A unique pickup identifier
     * @type {string}
     * @memberof Pickup
     */
    id?: string;
    /**
     * Specifies the object type
     * @type {string}
     * @memberof Pickup
     */
    object_type?: string;
    /**
     * The pickup carrier
     * @type {string}
     * @memberof Pickup
     */
    carrier_name: string;
    /**
     * The pickup carrier configured name
     * @type {string}
     * @memberof Pickup
     */
    carrier_id: string;
    /**
     * The pickup confirmation identifier
     * @type {string}
     * @memberof Pickup
     */
    confirmation_number: string;
    /**
     * The pickup date
     * @type {string}
     * @memberof Pickup
     */
    pickup_date?: string | null;
    /**
     * 
     * @type {Charge}
     * @memberof Pickup
     */
    pickup_charge?: Charge;
    /**
     * The pickup expected ready time
     * @type {string}
     * @memberof Pickup
     */
    ready_time?: string | null;
    /**
     * The pickup expected closing or late time
     * @type {string}
     * @memberof Pickup
     */
    closing_time?: string | null;
    /**
     * 
     * @type {Address}
     * @memberof Pickup
     */
    address: Address;
    /**
     * The shipment parcels to pickup.
     * @type {Array<Parcel>}
     * @memberof Pickup
     */
    parcels: Array<Parcel>;
    /**
     * 
     * The pickup instruction.
     * 
     * eg: Handle with care.
     * @type {string}
     * @memberof Pickup
     */
    instruction?: string | null;
    /**
     * 
     * The package(s) location.
     * 
     * eg: Behind the entrance door.
     * @type {string}
     * @memberof Pickup
     */
    package_location?: string | null;
    /**
     * Advanced carrier specific pickup options
     * @type {object}
     * @memberof Pickup
     */
    options?: object | null;
    /**
     * User metadata for the pickup
     * @type {object}
     * @memberof Pickup
     */
    metadata?: object;
    /**
     * Specified whether it was created with a carrier in test mode
     * @type {boolean}
     * @memberof Pickup
     */
    test_mode: boolean;
}

export function PickupFromJSON(json: any): Pickup {
    return PickupFromJSONTyped(json, false);
}

export function PickupFromJSONTyped(json: any, ignoreDiscriminator: boolean): Pickup {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': !exists(json, 'id') ? undefined : json['id'],
        'object_type': !exists(json, 'object_type') ? undefined : json['object_type'],
        'carrier_name': json['carrier_name'],
        'carrier_id': json['carrier_id'],
        'confirmation_number': json['confirmation_number'],
        'pickup_date': !exists(json, 'pickup_date') ? undefined : json['pickup_date'],
        'pickup_charge': !exists(json, 'pickup_charge') ? undefined : ChargeFromJSON(json['pickup_charge']),
        'ready_time': !exists(json, 'ready_time') ? undefined : json['ready_time'],
        'closing_time': !exists(json, 'closing_time') ? undefined : json['closing_time'],
        'address': AddressFromJSON(json['address']),
        'parcels': ((json['parcels'] as Array<any>).map(ParcelFromJSON)),
        'instruction': !exists(json, 'instruction') ? undefined : json['instruction'],
        'package_location': !exists(json, 'package_location') ? undefined : json['package_location'],
        'options': !exists(json, 'options') ? undefined : json['options'],
        'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
        'test_mode': json['test_mode'],
    };
}

export function PickupToJSON(value?: Pickup | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'object_type': value.object_type,
        'carrier_name': value.carrier_name,
        'carrier_id': value.carrier_id,
        'confirmation_number': value.confirmation_number,
        'pickup_date': value.pickup_date,
        'pickup_charge': ChargeToJSON(value.pickup_charge),
        'ready_time': value.ready_time,
        'closing_time': value.closing_time,
        'address': AddressToJSON(value.address),
        'parcels': ((value.parcels as Array<any>).map(ParcelToJSON)),
        'instruction': value.instruction,
        'package_location': value.package_location,
        'options': value.options,
        'metadata': value.metadata,
        'test_mode': value.test_mode,
    };
}

