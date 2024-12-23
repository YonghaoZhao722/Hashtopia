import http from "@/utils/http";

export const login = ({email, password}) => {
    return http({
        url: '/login/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            email,
            password
        }
    })
}

export const Register = ({email, username, password}) => {
    return http({
        url: '/register/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            username,
            password,
            email
        }
    })
}

export const changePassword = ({oldPassword, newPassword}) => {
    return http({
        url: '/change-password/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        data: {
            old_password: oldPassword,
            new_password: newPassword
        }
    })
}

export const queryUserIndex = ({id}) => {
    return http({
        url: '/index/',
        method: 'POST',
        data: {
            id
        }
    })
}

export const uploadPost = (data) => {
    return http({
        url: '/upload/info/',
        method: 'POST',
        data: data
    })
}

export const postDetail = ({id}) => {
    return http({
        url: '/post/detail/',
        method: 'POST',
        data: {
            id
        }
    })
}

export const queryPost = ({offset, query}) => {
    return http({
        url: '/post/',
        method: 'POST',
        data: {offset, query}
    })
}

export const doComment = ({data}) => {
    return http({
        url: '/comment/',
        method: 'POST',
        data: data
    })
}

export const doFocus = ({id}) => {
    return http({
        url: '/focus/',
        method: 'POST',
        data: {id}
    })
}

export const queryUserFocus = () => {
    return http({
        url: '/user/focus/',
    })
}

export const unFollow = ({id}) => {
    return http({
        url: '/user/unfollow/',
        method: 'POST',
        data: {id}
    })
}

export const updateUserInfo = ({username, signature}) => {
    return http({
        url: '/user/update/',
        method: 'POST',
        data: {
            username,
            signature
        }
    })
}

export const queryUserPost = ({user_id, types, offset}) => {
    return http({
        url: '/user/post/',
        method: 'POST',
        data: {
            user_id,
            types,
            offset
        }
    })
}

export const controlUserCollectOrLike = ({post_id, operator, type}) => {
    return http({
        url: '/post/control/',
        method: 'POST',
        data: {
            post_id,
            type,
            operator
        }
    })
}

export const getComment = ({id, offset}) => {
    return http({
        url: '/comment/main/',
        method: 'POST',
        data: {
            id,
            offset
        }
    })
}

export const queryUserPostControl = ({offset, types}) => {
    return http({
        url: '/user/post/control/',
        method: 'POST',
        data: {
            offset,
            types
        }
    })
}

export const postDelete = ({id}) => {
    return http({
        url: '/post/delete/',
        method: 'POST',
        data: {
            id
        }
    })
}

export const removeFan = ({id}) => {
    return http({
        url: '/user/remove/fan/',
        method: 'POST',
        data: {
            id
        }
    })
}

export const loadReplies = ({id, offset}) => {
    return http({
        url: '/comment/reply/',
        method: 'POST',
        data: {
            id,
            offset
        }
    })
}
