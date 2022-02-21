from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty


def async_relationship(
        argument,
        secondary=None,
        primaryjoin=None,
        secondaryjoin=None,
        foreign_keys=None,
        uselist=None,
        order_by=False,
        backref=None,
        back_populates=None,
        overlaps=None,
        post_update=False,
        cascade=False,
        viewonly=False,
        lazy="noload",
        collection_class=None,
        passive_deletes=True,
        passive_updates=True,
        remote_side=None,
        enable_typechecks=True,
        join_depth=None,
        comparator_factory=None,
        single_parent=False,
        innerjoin=False,
        distinct_target_key=None,
        doc=None,
        active_history=False,
        cascade_backrefs=True,
        load_on_pending=False,
        bake_queries=True,
        _local_remote_pairs=None,
        query_class=None,
        info=None,
        omit_join=None,
        sync_backref=None,
        _legacy_inactive_history_style=False,
) -> RelationshipProperty:
    """
    SqlAlchemy relationship optimized for async engine and with improved hinting
    Lazy loading example:
        class A(db.BaseModel):
            b = db.async_relationship("B", back_populates="a")
        class B(db.BaseModel):
            a_id = Column(Integer, ForeignKey(ForeignKey("a.id", ondelete="CASCADE")))
            a = db.async_relationship("A", back_populates="bs")
        # Fetching on loaded model
        model_a = await session.get(A, 1)
        model_b = db.load_one_relation()
        # Fetching in select query
        query = select(A).options(joinedload(A.b))
        result = await session.execute(query)
        model_a = result.scalars().one_or_none()
        model_b = model_a.b
    :param argument:
    :param secondary:
    :param primaryjoin:
    :param secondaryjoin:
    :param foreign_keys:
    :param uselist:
    :param order_by:
    :param backref:
    :param back_populates:
    :param overlaps:
    :param post_update:
    :param cascade:
    :param viewonly:
    :param lazy:
    :param collection_class:
    :param passive_deletes:
    :param passive_updates:
    :param remote_side:
    :param enable_typechecks:
    :param join_depth:
    :param comparator_factory:
    :param single_parent:
    :param innerjoin:
    :param distinct_target_key:
    :param doc:
    :param active_history:
    :param cascade_backrefs:
    :param load_on_pending:
    :param bake_queries:
    :param _local_remote_pairs:
    :param query_class:
    :param info:
    :param omit_join:
    :param sync_backref:
    :param _legacy_inactive_history_style:
    :return:
    """
    return relationship(
        argument,
        secondary=secondary,
        primaryjoin=primaryjoin,
        secondaryjoin=secondaryjoin,
        foreign_keys=foreign_keys,
        uselist=uselist,
        order_by=order_by,
        backref=backref,
        back_populates=back_populates,
        overlaps=overlaps,
        post_update=post_update,
        cascade=cascade,
        viewonly=viewonly,
        lazy=lazy,
        collection_class=collection_class,
        passive_deletes=passive_deletes,
        passive_updates=passive_updates,
        remote_side=remote_side,
        enable_typechecks=enable_typechecks,
        join_depth=join_depth,
        comparator_factory=comparator_factory,
        single_parent=single_parent,
        innerjoin=innerjoin,
        distinct_target_key=distinct_target_key,
        doc=doc,
        active_history=active_history,
        cascade_backrefs=cascade_backrefs,
        load_on_pending=load_on_pending,
        bake_queries=bake_queries,
        _local_remote_pairs=_local_remote_pairs,
        query_class=query_class,
        info=info,
        omit_join=omit_join,
        sync_backref=sync_backref,
        _legacy_inactive_history_style=_legacy_inactive_history_style
    )
