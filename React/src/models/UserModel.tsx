export interface UserModel {
    [key: string]: string | boolean; // Add an index signature to support dynamic property access
    id: string,
    email: string,
    username: string,
    first_name: string,
    last_name: string,
    created_at: string,
    is_admin: boolean,
    company_id: string
}

export interface UserParamModel {
    email: string | undefined,
    username: string | undefined,
    first_name: string | undefined,
    last_name: string | undefined,
    page: number,
    size: number
}