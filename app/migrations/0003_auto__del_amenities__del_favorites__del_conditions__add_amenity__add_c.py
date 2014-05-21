# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Amenities'
        db.delete_table(u'app_amenities')

        # Removing M2M table for field facility on 'Amenities'
        db.delete_table(db.shorten_name(u'app_amenities_facility'))

        # Deleting model 'Favorites'
        db.delete_table(u'app_favorites')

        # Deleting model 'Conditions'
        db.delete_table(u'app_conditions')

        # Removing M2M table for field facility on 'Conditions'
        db.delete_table(db.shorten_name(u'app_conditions_facility'))

        # Adding model 'Amenity'
        db.create_table(u'app_amenity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'app', ['Amenity'])

        # Adding M2M table for field facility on 'Amenity'
        m2m_table_name = db.shorten_name(u'app_amenity_facility')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('amenity', models.ForeignKey(orm[u'app.amenity'], null=False)),
            ('facility', models.ForeignKey(orm[u'app.facility'], null=False))
        ))
        db.create_unique(m2m_table_name, ['amenity_id', 'facility_id'])

        # Adding model 'Condition'
        db.create_table(u'app_condition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'app', ['Condition'])

        # Adding M2M table for field facility on 'Condition'
        m2m_table_name = db.shorten_name(u'app_condition_facility')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('condition', models.ForeignKey(orm[u'app.condition'], null=False)),
            ('facility', models.ForeignKey(orm[u'app.facility'], null=False))
        ))
        db.create_unique(m2m_table_name, ['condition_id', 'facility_id'])

        # Adding model 'Favorite'
        db.create_table(u'app_favorite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Facility'])),
        ))
        db.send_create_signal(u'app', ['Favorite'])

        # Adding field 'Fee.name'
        db.add_column(u'app_fee', 'name',
                      self.gf('django.db.models.fields.CharField')(default='doop', max_length=50),
                      keep_default=False)

        # Adding field 'RoomType.care_type'
        db.add_column(u'app_roomtype', 'care_type',
                      self.gf('django.db.models.fields.CharField')(default='poop', max_length='20'),
                      keep_default=False)

        # Adding M2M table for field facility on 'RoomType'
        m2m_table_name = db.shorten_name(u'app_roomtype_facility')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('roomtype', models.ForeignKey(orm[u'app.roomtype'], null=False)),
            ('facility', models.ForeignKey(orm[u'app.facility'], null=False))
        ))
        db.create_unique(m2m_table_name, ['roomtype_id', 'facility_id'])


    def backwards(self, orm):
        # Adding model 'Amenities'
        db.create_table(u'app_amenities', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'app', ['Amenities'])

        # Adding M2M table for field facility on 'Amenities'
        m2m_table_name = db.shorten_name(u'app_amenities_facility')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('amenities', models.ForeignKey(orm[u'app.amenities'], null=False)),
            ('facility', models.ForeignKey(orm[u'app.facility'], null=False))
        ))
        db.create_unique(m2m_table_name, ['amenities_id', 'facility_id'])

        # Adding model 'Favorites'
        db.create_table(u'app_favorites', (
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Facility'])),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'app', ['Favorites'])

        # Adding model 'Conditions'
        db.create_table(u'app_conditions', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'app', ['Conditions'])

        # Adding M2M table for field facility on 'Conditions'
        m2m_table_name = db.shorten_name(u'app_conditions_facility')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('conditions', models.ForeignKey(orm[u'app.conditions'], null=False)),
            ('facility', models.ForeignKey(orm[u'app.facility'], null=False))
        ))
        db.create_unique(m2m_table_name, ['conditions_id', 'facility_id'])

        # Deleting model 'Amenity'
        db.delete_table(u'app_amenity')

        # Removing M2M table for field facility on 'Amenity'
        db.delete_table(db.shorten_name(u'app_amenity_facility'))

        # Deleting model 'Condition'
        db.delete_table(u'app_condition')

        # Removing M2M table for field facility on 'Condition'
        db.delete_table(db.shorten_name(u'app_condition_facility'))

        # Deleting model 'Favorite'
        db.delete_table(u'app_favorite')

        # Deleting field 'Fee.name'
        db.delete_column(u'app_fee', 'name')

        # Deleting field 'RoomType.care_type'
        db.delete_column(u'app_roomtype', 'care_type')

        # Removing M2M table for field facility on 'RoomType'
        db.delete_table(db.shorten_name(u'app_roomtype_facility'))


    models = {
        u'account.holdinggroup': {
            'Meta': {'object_name': 'HoldingGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'app.amenity': {
            'Meta': {'object_name': 'Amenity'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'amenities'", 'symmetrical': 'False', 'to': u"orm['app.Facility']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.condition': {
            'Meta': {'object_name': 'Condition'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'conditions'", 'symmetrical': 'False', 'to': u"orm['app.Facility']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.facility': {
            'Meta': {'object_name': 'Facility'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'care_level_1_cost': ('django.db.models.fields.IntegerField', [], {}),
            'care_level_2_cost': ('django.db.models.fields.IntegerField', [], {}),
            'care_level_3_cost': ('django.db.models.fields.IntegerField', [], {}),
            'care_memory_cost': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description_long': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'description_short': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'director_avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'director_email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'director_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'facility_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.FacilityType']", 'symmetrical': 'False'}),
            'favorited_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.User']", 'through': u"orm['app.Favorite']", 'symmetrical': 'False'}),
            'holding_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.HoldingGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.IntegerField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'longitude': ('django.db.models.fields.IntegerField', [], {}),
            'medication_level_1_cost': ('django.db.models.fields.IntegerField', [], {}),
            'medication_level_2_cost': ('django.db.models.fields.IntegerField', [], {}),
            'medication_level_3_cost': ('django.db.models.fields.IntegerField', [], {}),
            'min_price': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shown_on_home': ('django.db.models.fields.BooleanField', [], {}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "['name', 'zipcode']", 'overwrite': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        u'app.facilityfee': {
            'Meta': {'object_name': 'FacilityFee'},
            'cost': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            'fee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Fee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'app.facilityimage': {
            'Meta': {'object_name': 'FacilityImage'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'app.facilitymessage': {
            'Meta': {'object_name': 'FacilityMessage'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'replied_by': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'replied_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'app.facilitytype': {
            'Meta': {'object_name': 'FacilityType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'app.favorite': {
            'Meta': {'object_name': 'Favorite'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'app.fee': {
            'Meta': {'object_name': 'Fee'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Facility']", 'through': u"orm['app.FacilityFee']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'app.inquiry': {
            'Meta': {'object_name': 'Inquiry'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'est_move': ('django.db.models.fields.DateField', [], {}),
            'from_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'remind': ('django.db.models.fields.BooleanField', [], {})
        },
        u'app.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'contact_person_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_person_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contact_person_phone': ('django.db.models.fields.IntegerField', [], {}),
            'contact_person_relationship': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            'holding_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.HoldingGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'move_in_date': ('django.db.models.fields.DateTimeField', [], {}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'resident_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': "'20'"})
        },
        u'app.language': {
            'Meta': {'object_name': 'Language'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'languages'", 'symmetrical': 'False', 'to': u"orm['app.Facility']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.roomtype': {
            'Meta': {'object_name': 'RoomType'},
            'care_type': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'room_types'", 'symmetrical': 'False', 'to': u"orm['app.Facility']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'square_footage': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'starting_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'unit_type': ('django.db.models.fields.CharField', [], {'max_length': "'20'"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']