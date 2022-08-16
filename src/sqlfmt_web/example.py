# flake8: noqa
EXAMPLE = """
with source as (select * from {{ source('my_application', 'users') }}),
  renamed as ( select
      --ids
      id,
      NULLIF(xid,'') as xid,

      --dates
      created_on, updated_on,

      NULLIF(email,'') as email,
      
      -- names
      NULLIF(full_name,'') as full_name,
      NULLIF(trim(case when regexp_count(nullif(full_name,''), ' ') = 0 then nullif(full_name,'')
        when regexp_count(nullif(full_name,''), ' ') = 1 then split_part(nullif(full_name,''), ' ', 1)
        else regexp_substr(nullif(full_name,''), '.* .* ') -- this user has more than two names!
        end
      ), 'TEST_USER') as first_name,
      nullif(split_part(nullif(full_name,''), ' ', greatest(2, regexp_count(nullif(full_name,''), ' ')+1)),'') as last_name

    FROM
    source

    where nvl(is_deleted, false) is false
      and id <> 123456 -- a very long comment about why we would exclude this user from this table that we will wrap

  )
select * from renamed
""".lstrip()
