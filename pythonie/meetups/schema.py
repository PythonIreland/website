import colander


class Meetups(colander.MappingSchema):
    class meta(colander.MappingSchema):
        lat = colander.SchemaNode(colander.String())
        lon = colander.SchemaNode(colander.String())
        updated = colander.SchemaNode(colander.DateTime())
        title = colander.SchemaNode(colander.String())
        description = colander.SchemaNode(colander.String())
        count = colander.SchemaNode(colander.Integer())
        link = colander.SchemaNode(colander.String())
        total_count = colander.SchemaNode(colander.Integer())
        url = colander.SchemaNode(colander.String())

    @colander.instantiate()
    class results(colander.SequenceSchema):
        @colander.instantiate()
        class result(colander.MappingSchema):
            id = colander.SchemaNode(colander.String())
            event_url = colander.SchemaNode(colander.String())
            announced = colander.SchemaNode(colander.Boolean())
            status = colander.SchemaNode(colander.String())
            updated = colander.SchemaNode(colander.Integer())

            @colander.instantiate()
            class group(colander.MappingSchema):
                who = colander.SchemaNode(colander.String())
                join_mode = colander.SchemaNode(colander.String())
                id = colander.SchemaNode(colander.Integer())
                name = colander.SchemaNode(colander.String())
                urlname = colander.SchemaNode(colander.String())
                group_lon = colander.SchemaNode(colander.Float())
                group_lat = colander.SchemaNode(colander.Float())
                created = colander.SchemaNode(colander.Integer())

            time = colander.SchemaNode(colander.Integer())
            utc_offset = colander.SchemaNode(colander.Integer())

            @colander.instantiate(missing=colander.drop)
            class venue(colander.MappingSchema):
                city = colander.SchemaNode(colander.String())
                lon = colander.SchemaNode(colander.Float())
                repinned = colander.SchemaNode(colander.Boolean())
                lat = colander.SchemaNode(colander.Float())
                id = colander.SchemaNode(colander.Float())
                name = colander.SchemaNode(colander.String())
                address_1 = colander.SchemaNode(colander.String())
                country = colander.SchemaNode(colander.String())

            name = colander.SchemaNode(colander.String())
            headcount = colander.SchemaNode(colander.Integer())
            description = colander.SchemaNode(colander.String())
            visibility = colander.SchemaNode(colander.String())
            created = colander.SchemaNode(colander.Integer())
            duration = colander.SchemaNode(colander.Integer(), missing=colander.drop)

            maybe_rsvp_count = colander.SchemaNode(colander.Integer())
            yes_rsvp_count = colander.SchemaNode(colander.Integer())
            rsvp_limit = colander.SchemaNode(colander.Integer(), missing=colander.drop)
            waitlist_count = colander.SchemaNode(colander.Integer())

