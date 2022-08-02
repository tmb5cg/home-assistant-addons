# Monkeypox Vaccine Appointment Detector MQTT Bridge hass.io addon

Add-on for detecting vaccine appointment availability by crawing [Vax4NYC portal](https://vax4nyc.nyc.gov/patient/s/vaccination-schedule?page=Monkeypox) and notifies availability via SMS.

## Configuration

Add-on configuration example:

```yaml
email: example@email.com
password: '!secret oru_password'
mfa_type: TOTP
mfa_secret: '!secret oru_mfa_secret'
account_uuid: ef788d65-5380-11e8-8211-2655115779ac
meter_number: 706438804
site: oru
mqtt_host: hassio.local
mqtt_user: mqtt
mqtt_password: '!secret mqtt_password'
```

### Option: `mqtt_host`

Defines the hostname or ip of the MQTT server

### Option: `mqtt_user`

Defines the username for the MQTT server

### Option: `mqtt_password`

Defines the password for the MQTT server


## MQTT Data

The addon will publish the latest meter read value and unit of measure to the following topics:

`monkeypox/startTime`


## Home Assistant Energy

To enable tracking of your power usage with the new (as of 08/2021) Home Assistant Energy panel, you must add the following to your `configuration.yaml`:

```yaml

homeassistant:
  ...
  customize_glob:
    sensor.*_energy:
      last_reset: '1970-01-01T00:00:00+00:00'
      device_class: energy
      state_class: measurement

sensor:
  ...
  - platform: mqtt
    name: "ConEd Energy Usage"
    unique_id: "coned_energy"
    state_topic: "electric_meter/value"
    unit_of_measurement: 'kWh'
    device_class: energy
    state_class: measurement

```
