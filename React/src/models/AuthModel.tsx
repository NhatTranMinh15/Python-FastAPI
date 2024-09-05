export type LogInModel = {
    username: string,
    password: string,
}

export type LogInResponseModel = {
    access_token: string,
    token_type: string
}

export type ChangePasswordModel = {
    oldPassword: string,
    newPassword: string
}