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
/**
 * 
 * @export
 * @interface ShipmentRateData
 */
export interface ShipmentRateData {
    /**
     * 
     * The requested carrier service for the shipment.
     * 
     * Please consult [the reference](#operation/references) for specific carriers services.<br/>
     * Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.
     * @type {Array<string>}
     * @memberof ShipmentRateData
     */
    services?: Array<string> | null;
    /**
     * 
     * The list of configured carriers you wish to get rates from.
     * 
     * *Note that the request will be sent to all carriers in nothing is specified*
     * @type {Array<string>}
     * @memberof ShipmentRateData
     */
    carrier_ids?: Array<string> | null;
    /**
     * The shipment reference
     * @type {string}
     * @memberof ShipmentRateData
     */
    reference?: string | null;
    /**
     * User metadata for the shipment
     * @type {object}
     * @memberof ShipmentRateData
     */
    metadata?: object;
}

export function ShipmentRateDataFromJSON(json: any): ShipmentRateData {
    return ShipmentRateDataFromJSONTyped(json, false);
}

export function ShipmentRateDataFromJSONTyped(json: any, ignoreDiscriminator: boolean): ShipmentRateData {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'services': !exists(json, 'services') ? undefined : json['services'],
        'carrier_ids': !exists(json, 'carrier_ids') ? undefined : json['carrier_ids'],
        'reference': !exists(json, 'reference') ? undefined : json['reference'],
        'metadata': !exists(json, 'metadata') ? undefined : json['metadata'],
    };
}

export function ShipmentRateDataToJSON(value?: ShipmentRateData | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'services': value.services,
        'carrier_ids': value.carrier_ids,
        'reference': value.reference,
        'metadata': value.metadata,
    };
}

