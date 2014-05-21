# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Facility'
        db.create_table(u'app_facility', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('holding_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.HoldingGroup'])),
            ('director_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('director_email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('director_avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
            ('min_price', self.gf('django.db.models.fields.IntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from=['name', 'zipcode'], overwrite=False)),
            ('latitude', self.gf('django.db.models.fields.IntegerField')()),
            ('longitude', self.gf('django.db.models.fields.IntegerField')()),
            ('shown_on_home', self.gf('django.db.models.fields.BooleanField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length='20')),
            ('description_short', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('description_long', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('care_level_1_cost', self.gf('django.db.models.fields.IntegerField')()),
            ('care_level_2_cost', self.gf('django.db.models.fields.IntegerField')()),
            ('care_level_3_cost', self.gf('django.db.models.fields.IntegerField')()),
            ('care_memory_cost', self.gf('django.db.models.fields.IntegerField')()),
            ('medication_level_1_cost', self.gf('django.db.models.fields.IntegerField')()),
            ('medication_level_2_cost', self.gf('django.db.models.fields.IntegerField')()),
            ('medication_level_3_cost', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'app', ['Facility'])

        # Adding M2M table for field facility_types on 'Facility'
        m2m_table_name = db.shorten_name(u'app_facility_facility_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('facility', models.ForeignKey(orm[u'app.facility'], null=False)),
            ('facilitytype', models.ForeignKey(orm[u'app.facilitytype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['facility_id', 'facilitytype_id'])

        # Adding model 'FacilityFee'
        db.create_table(u'app_facilityfee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Facility'])),
            ('fee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Fee'])),
            ('cost', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'app', ['FacilityFee'])

        # Adding model 'Fee'
        db.create_table(u'app_fee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'app', ['Fee'])

        # Adding model 'FacilityMessage'
        db.create_table(u'app_facilitymessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('replied_by', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('replied_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'app', ['FacilityMessage'])

        # Adding model 'FacilityType'
        db.create_table(u'app_facilitytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'app', ['FacilityType'])

        # Adding model 'Language'
        db.create_table(u'app_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'app', ['Language'])

        # Adding M2M table for field facility on 'Language'
        m2m_table_name = db.shorten_name(u'app_language_facility')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('language', models.ForeignKey(orm[u'app.language'], null=False)),
            ('facility', models.ForeignKey(orm[u'app.facility'], null=False))
        ))
        db.create_unique(m2m_table_name, ['language_id', 'facility_id'])

        # Adding model 'Conditions'
        db.create_table(u'app_conditions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
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

        # Adding model 'Amenities'
        db.create_table(u'app_amenities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
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

        # Adding model 'RoomType'
        db.create_table(u'app_roomtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('unit_type', self.gf('django.db.models.fields.CharField')(max_length='20')),
            ('starting_price', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('square_footage', self.gf('django.db.models.fields.CharField')(max_length='20')),
        ))
        db.send_create_signal(u'app', ['RoomType'])

        # Adding model 'FacilityImage'
        db.create_table(u'app_facilityimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Facility'])),
            ('featured', self.gf('django.db.models.fields.BooleanField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'app', ['FacilityImage'])

        # Adding model 'Inquiry'
        db.create_table(u'app_inquiry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('from_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('est_move', self.gf('django.db.models.fields.DateField')()),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('remind', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'app', ['Inquiry'])

        # Adding model 'Invoice'
        db.create_table(u'app_invoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('holding_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.HoldingGroup'])),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Facility'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length='20')),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length='20')),
            ('contact_person_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact_person_relationship', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_person_phone', self.gf('django.db.models.fields.IntegerField')()),
            ('contact_person_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('move_in_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('resident_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'app', ['Invoice'])

        # Adding model 'Favorites'
        db.create_table(u'app_favorites', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
            ('facility', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Facility'])),
        ))
        db.send_create_signal(u'app', ['Favorites'])


    def backwards(self, orm):
        # Deleting model 'Facility'
        db.delete_table(u'app_facility')

        # Removing M2M table for field facility_types on 'Facility'
        db.delete_table(db.shorten_name(u'app_facility_facility_types'))

        # Deleting model 'FacilityFee'
        db.delete_table(u'app_facilityfee')

        # Deleting model 'Fee'
        db.delete_table(u'app_fee')

        # Deleting model 'FacilityMessage'
        db.delete_table(u'app_facilitymessage')

        # Deleting model 'FacilityType'
        db.delete_table(u'app_facilitytype')

        # Deleting model 'Language'
        db.delete_table(u'app_language')

        # Removing M2M table for field facility on 'Language'
        db.delete_table(db.shorten_name(u'app_language_facility'))

        # Deleting model 'Conditions'
        db.delete_table(u'app_conditions')

        # Removing M2M table for field facility on 'Conditions'
        db.delete_table(db.shorten_name(u'app_conditions_facility'))

        # Deleting model 'Amenities'
        db.delete_table(u'app_amenities')

        # Removing M2M table for field facility on 'Amenities'
        db.delete_table(db.shorten_name(u'app_amenities_facility'))

        # Deleting model 'RoomType'
        db.delete_table(u'app_roomtype')

        # Deleting model 'FacilityImage'
        db.delete_table(u'app_facilityimage')

        # Deleting model 'Inquiry'
        db.delete_table(u'app_inquiry')

        # Deleting model 'Invoice'
        db.delete_table(u'app_invoice')

        # Deleting model 'Favorites'
        db.delete_table(u'app_favorites')


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
        u'app.amenities': {
            'Meta': {'object_name': 'Amenities'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Facility']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.conditions': {
            'Meta': {'object_name': 'Conditions'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Facility']", 'symmetrical': 'False'}),
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
            'favorited_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['account.User']", 'through': u"orm['app.Favorites']", 'symmetrical': 'False'}),
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
        u'app.favorites': {
            'Meta': {'object_name': 'Favorites'},
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
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
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
            'facility': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Facility']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.roomtype': {
            'Meta': {'object_name': 'RoomType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
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