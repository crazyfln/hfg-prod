# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    needed_by = (
            ("reversion", "0001_initial"),
            ("app", "0001_initial"),
    )

    needed_by = (
        ("reversion", "0001_initial"),
        ("app", "0001_initial"),

    )


    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'account_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('searching_for', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('budget', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('pay_private_pay', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pay_longterm_care', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pay_veterans_benefits', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pay_medicare', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pay_medicaid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pay_ssi', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_bathing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_diabetic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_mobility', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('care_current', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('care_medical_assistance', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_toileting', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_memory_issues', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_diagnosed_memory', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_combinative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('care_wandering', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('desired_city', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('resident_first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('health_description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('planned_move_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('move_in_time_frame', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'account', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'account_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'account.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'account_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'account.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'HoldingGroup'
        db.create_table(u'account_holdinggroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'account', ['HoldingGroup'])

        # Adding model 'FacilityDirector'
        db.create_table(u'account_facilitydirector', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['account.User'], unique=True, primary_key=True)),
            ('holding_group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owners', to=orm['account.HoldingGroup'])),
        ))
        db.send_create_signal(u'account', ['FacilityDirector'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'account_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'account_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'account_user_user_permissions'))

        # Deleting model 'HoldingGroup'
        db.delete_table(u'account_holdinggroup')

        # Deleting model 'FacilityDirector'
        db.delete_table(u'account_facilitydirector')


    models = {
        u'account.facilitydirector': {
            'Meta': {'object_name': 'FacilityDirector', '_ormbases': [u'account.User']},
            'holding_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owners'", 'to': u"orm['account.HoldingGroup']"}),
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['account.User']", 'unique': 'True', 'primary_key': 'True'})
        },
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

    complete_apps = ['account']
