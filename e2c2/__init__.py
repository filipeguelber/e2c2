from e2c2 import E2C2


if __name__ == '__main__':

    module_e2c2 = E2C2()
    for user in module_e2c2.users:
        permission = module_e2c2.permissions[user]
        for key in permission:
            if permission[key] == 'u':
                module_e2c2.create_user_on_instance(user, key)
                module_e2c2.add_user_key_to_instance(user, key)
            else:
                module_e2c2.delete_user(user, key)