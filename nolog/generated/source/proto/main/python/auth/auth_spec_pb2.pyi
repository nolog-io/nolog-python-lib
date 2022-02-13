"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class ClientKey(google.protobuf.message.Message):
    """API Key"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class KeyFieldsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        value: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    KEY_FIELDS_FIELD_NUMBER: builtins.int
    @property
    def key_fields(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]: ...
    def __init__(self,
        *,
        key_fields : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["key_fields",b"key_fields"]) -> None: ...
global___ClientKey = ClientKey

class KeyContent(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class ContentFieldsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        value: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    CONTENT_FIELDS_FIELD_NUMBER: builtins.int
    @property
    def content_fields(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]: ...
    def __init__(self,
        *,
        content_fields : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["content_fields",b"content_fields"]) -> None: ...
global___KeyContent = KeyContent

class InternalAuthMetadata(google.protobuf.message.Message):
    """Auth Session Metadata"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class _AuthType:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _AuthTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_AuthType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
        PASSTHROUGH: InternalAuthMetadata.AuthType.ValueType = ...  # 0
        API_KEY: InternalAuthMetadata.AuthType.ValueType = ...  # 1
        USER: InternalAuthMetadata.AuthType.ValueType = ...  # 3
    class AuthType(_AuthType, metaclass=_AuthTypeEnumTypeWrapper):
        pass

    PASSTHROUGH: InternalAuthMetadata.AuthType.ValueType = ...  # 0
    API_KEY: InternalAuthMetadata.AuthType.ValueType = ...  # 1
    USER: InternalAuthMetadata.AuthType.ValueType = ...  # 3

    class UserAuth(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        class _UserAuthType:
            ValueType = typing.NewType('ValueType', builtins.int)
            V: typing_extensions.TypeAlias = ValueType
        class _UserAuthTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_UserAuthType.ValueType], builtins.type):
            DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
            ADMIN: InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...  # 0
            SAML: InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...  # 1
            GCP: InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...  # 2
        class UserAuthType(_UserAuthType, metaclass=_UserAuthTypeEnumTypeWrapper):
            pass

        ADMIN: InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...  # 0
        SAML: InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...  # 1
        GCP: InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...  # 2

        class SAMLUserMetadata(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            USERNAME_FIELD_NUMBER: builtins.int
            LAST_VALIDATED_AT_FIELD_NUMBER: builtins.int
            username: typing.Text = ...
            last_validated_at: builtins.int = ...
            def __init__(self,
                *,
                username : typing.Text = ...,
                last_validated_at : builtins.int = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["last_validated_at",b"last_validated_at","username",b"username"]) -> None: ...

        class GCPUserMetadata(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
            USERNAME_FIELD_NUMBER: builtins.int
            LAST_VALIDATED_AT_FIELD_NUMBER: builtins.int
            JWT_TOKEN_FIELD_NUMBER: builtins.int
            username: typing.Text = ...
            last_validated_at: builtins.int = ...
            jwt_token: typing.Text = ...
            def __init__(self,
                *,
                username : typing.Text = ...,
                last_validated_at : builtins.int = ...,
                jwt_token : typing.Text = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["jwt_token",b"jwt_token","last_validated_at",b"last_validated_at","username",b"username"]) -> None: ...

        USER_AUTH_TYPE_FIELD_NUMBER: builtins.int
        SAML_USER_FIELD_NUMBER: builtins.int
        GCP_USER_FIELD_NUMBER: builtins.int
        ADMIN_USER_FIELD_NUMBER: builtins.int
        user_auth_type: global___InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...
        @property
        def saml_user(self) -> global___InternalAuthMetadata.UserAuth.SAMLUserMetadata: ...
        @property
        def gcp_user(self) -> global___InternalAuthMetadata.UserAuth.GCPUserMetadata: ...
        @property
        def admin_user(self) -> global___InternalAuthMetadata.UserAuth.GCPUserMetadata: ...
        def __init__(self,
            *,
            user_auth_type : global___InternalAuthMetadata.UserAuth.UserAuthType.ValueType = ...,
            saml_user : typing.Optional[global___InternalAuthMetadata.UserAuth.SAMLUserMetadata] = ...,
            gcp_user : typing.Optional[global___InternalAuthMetadata.UserAuth.GCPUserMetadata] = ...,
            admin_user : typing.Optional[global___InternalAuthMetadata.UserAuth.GCPUserMetadata] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["admin_user",b"admin_user","gcp_user",b"gcp_user","saml_user",b"saml_user","user_metadata",b"user_metadata"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["admin_user",b"admin_user","gcp_user",b"gcp_user","saml_user",b"saml_user","user_auth_type",b"user_auth_type","user_metadata",b"user_metadata"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal["user_metadata",b"user_metadata"]) -> typing.Optional[typing_extensions.Literal["saml_user","gcp_user","admin_user"]]: ...

    AUTH_TYPE_FIELD_NUMBER: builtins.int
    CLIENT_ID_FIELD_NUMBER: builtins.int
    PASSTHROUGH_FIELD_NUMBER: builtins.int
    API_KEY_FIELD_NUMBER: builtins.int
    USER_AUTH_FIELD_NUMBER: builtins.int
    auth_type: global___InternalAuthMetadata.AuthType.ValueType = ...
    client_id: typing.Text = ...
    passthrough: builtins.bool = ...
    api_key: builtins.bool = ...
    @property
    def user_auth(self) -> global___InternalAuthMetadata.UserAuth: ...
    def __init__(self,
        *,
        auth_type : global___InternalAuthMetadata.AuthType.ValueType = ...,
        client_id : typing.Text = ...,
        passthrough : builtins.bool = ...,
        api_key : builtins.bool = ...,
        user_auth : typing.Optional[global___InternalAuthMetadata.UserAuth] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["api_key",b"api_key","auth_metadata",b"auth_metadata","passthrough",b"passthrough","user_auth",b"user_auth"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_key",b"api_key","auth_metadata",b"auth_metadata","auth_type",b"auth_type","client_id",b"client_id","passthrough",b"passthrough","user_auth",b"user_auth"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["auth_metadata",b"auth_metadata"]) -> typing.Optional[typing_extensions.Literal["passthrough","api_key","user_auth"]]: ...
global___InternalAuthMetadata = InternalAuthMetadata