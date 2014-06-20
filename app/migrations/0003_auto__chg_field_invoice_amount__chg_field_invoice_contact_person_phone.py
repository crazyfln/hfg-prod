# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Invoice.amount'
        db.alter_column(u'app_invoice', 'amount', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'Invoice.contact_person_phone'
        db.alter_column(u'app_invoice', 'contact_person_phone', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):

        # Changing field 'Invoice.amount'
        db.alter_column(u'app_invoice', 'amount', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Invoice.contact_person_phone'
        db.alter_column(u'app_invoice', 'contact_person_phone', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'account.holdinggroup': {
            'Meta': {'object_name': 'HoldingGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'account.user': {
            'Meta': {'object_name': 'User'},
            'budget': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_bathing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_combinative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_current': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_diabetic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_diagnosed_memory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_medical_assistance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_memory_issues': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_mobility': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_toileting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'care_wandering': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'desired_city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'health_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'holding_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owners'", 'null': 'True', 'to': u"orm['account.HoldingGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'move_in_time_frame': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pay_longterm_care': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_medicaid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_medicare': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_private_pay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_ssi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pay_veterans_benefits': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'planned_move_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'resident_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'searching_for': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'app.amenity': {
            'Meta': {'object_name': 'Amenity'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.condition': {
            'Meta': {'object_name': 'Condition'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'conditions'", 'blank': 'True', 'to': u"orm['account.User']"})
        },
        u'app.facility': {
            'Meta': {'object_name': 'Facility'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'amenities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'facilities'", 'symmetrical': 'False', 'to': u"orm['app.Amenity']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'care_level_1_cost': ('django.db.models.fields.IntegerField', [], {}),
            'care_level_2_cost': ('django.db.models.fields.IntegerField', [], {}),
            'care_level_3_cost': ('django.db.models.fields.IntegerField', [], {}),
            'care_memory_cost': ('django.db.models.fields.IntegerField', [], {}),
            'care_type': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'conditions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'facilities'", 'symmetrical': 'False', 'to': u"orm['app.Condition']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description_long': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'description_short': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'director_avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'director_email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'director_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'facility_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.FacilityType']", 'symmetrical': 'False'}),
            'favorited_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'favorites'", 'symmetrical': 'False', 'through': u"orm['app.Favorite']", 'to': u"orm['account.User']"}),
            'fees': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.Fee']", 'through': u"orm['app.FacilityFee']", 'symmetrical': 'False'}),
            'holding_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.HoldingGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'facilities'", 'symmetrical': 'False', 'to': u"orm['app.Language']"}),
            'latitude': ('django.db.models.fields.IntegerField', [], {}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'longitude': ('django.db.models.fields.IntegerField', [], {}),
            'medication_level_1_cost': ('django.db.models.fields.IntegerField', [], {}),
            'medication_level_2_cost': ('django.db.models.fields.IntegerField', [], {}),
            'medication_level_3_cost': ('django.db.models.fields.IntegerField', [], {}),
            'min_price': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phone_requested_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'phone_requests'", 'symmetrical': 'False', 'through': u"orm['app.PhoneRequest']", 'to': u"orm['account.User']"}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['app.RoomType']", 'through': u"orm['app.FacilityRoom']", 'symmetrical': 'False'}),
            'shown_on_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "['name', 'zipcode']", 'overwrite': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'vacancies': ('django.db.models.fields.IntegerField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['app.Facility']"}),
            'featured': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'app.facilitymessage': {
            'Meta': {'object_name': 'FacilityMessage'},
            'budget': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_bathing': ('django.db.models.fields.BooleanField', [], {}),
            'care_combinative': ('django.db.models.fields.BooleanField', [], {}),
            'care_current': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_diabetic': ('django.db.models.fields.BooleanField', [], {}),
            'care_diagnosed_memory': ('django.db.models.fields.BooleanField', [], {}),
            'care_medical_assistance': ('django.db.models.fields.BooleanField', [], {}),
            'care_memory_issues': ('django.db.models.fields.BooleanField', [], {}),
            'care_mobility': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'care_toileting': ('django.db.models.fields.BooleanField', [], {}),
            'care_wandering': ('django.db.models.fields.BooleanField', [], {}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'desired_city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            'health_description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'move_in_time_frame': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'pay_longterm_care': ('django.db.models.fields.BooleanField', [], {}),
            'pay_medicaid': ('django.db.models.fields.BooleanField', [], {}),
            'pay_medicare': ('django.db.models.fields.BooleanField', [], {}),
            'pay_private_pay': ('django.db.models.fields.BooleanField', [], {}),
            'pay_ssi': ('django.db.models.fields.BooleanField', [], {}),
            'pay_veterans_benefits': ('django.db.models.fields.BooleanField', [], {}),
            'planned_move_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'replied_by': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'replied_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'resident_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'searching_for': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'app.facilityroom': {
            'Meta': {'object_name': 'FacilityRoom'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'room_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.RoomType']"}),
            'starting_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '5'})
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
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'billed_on': ('django.db.models.fields.DateTimeField', [], {}),
            'contact_person_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'contact_person_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contact_person_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'contact_person_relationship': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            'holding_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.HoldingGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'move_in_date': ('django.db.models.fields.DateTimeField', [], {}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': "'20'"}),
            'recieved': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'resident_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': "'20'"})
        },
        u'app.language': {
            'Meta': {'object_name': 'Language'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'app.phonerequest': {
            'Meta': {'object_name': 'PhoneRequest'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Facility']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.User']"})
        },
        u'app.roomtype': {
            'Meta': {'object_name': 'RoomType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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