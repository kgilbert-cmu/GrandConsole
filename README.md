# GrandConsole
Dump custom Facebook Group summary stats using Graph API

## Setup
Touch `local_config.py` and insert entries for your desired group ID (specified as `ID`) and an Facebook Graph API developers token (specified as `access_token`). An example file `local_config.example` is provided.

If the target group has a permalink name, make sure to use the numerical group ID, which you can find by clicking on 'Manage Group' in the left-panel of the group page.

If the target group is set to CLOSED privacy, make sure that the access token is generated with an account that has ADMIN rights to the group.

Make sure that your token is generated using the `user_managed_groups` option.

