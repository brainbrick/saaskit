import argparse
import requests

def restore_database(master_pwd, name, endpoint_url, backup_file_path, copy):
    try:
        # Endpoint URL
        post_url = endpoint_url+'/web/database/restore'

        # Prepare parameters for the request
        params = {
            "master_pwd": master_pwd,
            "name": name,
            "copy": copy
        }
        full_file_path = '/home/ins/backup/upload/' + backup_file_path

        # Open the backup file for upload
        files = {'backup_file': open(full_file_path, 'rb')}

        # Making a POST request using requests library
        response = requests.post(post_url, params=params, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            # Check if the response contains a success message
            if "Database restored successfully" in response.text:
                return_value = 'success:: message: Database restored successfully.'
                return return_value
            else:
                # Check for specific error messages in the HTML response
                if "Database already exists" in response.text:
                    return_value = 'success:error:: message: Database restore error: Database already exists'
                    return return_value
                elif "Access Denied" in response.text:
                    return_value = 'success:error:: message: Database restore error: Access Denied'
                    return return_value
                elif response.status_code == 200:
                    return_value = 'success:: message: Database restored successfully.'
                    return return_value
                else:
                    return_value = 'success:error:: message: Failed to restore database. Reason: {}' + format(response.status_code)
                    return return_value
            
        else:
            return_value = 'success:error:: message: Failed to restore database. Status code: {}' + format(response.status_code)
            return return_value
    except Exception as e:
        return_value = 'success:error:: message: Failed to restore database. Reason: {}' + format(str(e))
        return return_value

if __name__ == "__main__":
# Example usage:
    parser = argparse.ArgumentParser(description='Restore a database from a backup file')
    
    parser.add_argument('master_pwd', type=str, help='Master password')
    parser.add_argument('name', type=str, help='New database name')
    parser.add_argument('endpoint_url', type=str, help='Endpoint URL')
    parser.add_argument('backup_file_path', type=str, help='Backup file path')
    parser.add_argument('copy', type=str, help='Copy database if it already exists')

    args = parser.parse_args()

    master_pwd = args.master_pwd
    name = args.name
    endpoint_url = args.endpoint_url
    backup_file_path = args.backup_file_path
    copy = args.copy
    
    
    

    # Call the restore_database function with the provided parameters
    response = restore_database(master_pwd, name, endpoint_url, backup_file_path, copy)

    # Print the response
    print(response)