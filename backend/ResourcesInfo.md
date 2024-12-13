# Rest api resouce access declaration

|Method HTTP| URI | Action|
|-----------|-----|-------|
|GET| http://[hostname]/api/login | login request|
|GET| http://[hostname]/api/register | register request|
|GET| http://[hostname]/api/requests/[access] | get list of available requests for pointed access |
|GET| http://[hostname]/api/marks | Get list of existing marks |
|GET| http://[hostname]/api/marks/[mark_id] | Get data of mark with mark_id |
|POST| http://[hostname]/api/marks/[mark_id] | Change data of mark with mark_id |
|PUT| http://[hostname]/api/marks/[mark_id] | Add new mark with with mark_id |
|DELETE| http://[hostname]/api/marks/[mark_id] | Delete mark with with mark_id |

# Resources Structure

## User
|Field| type | desc |
|-----|------|----- |
|id| int| uniquer user's id|
|role_id|int| used for access level managment(FK: Privileges.id)|
|login(nullable)| varchar| user login(redactor/admins only)|
|password(nullable, hashed)|varchar | hashed password(redactor/admins only)|
