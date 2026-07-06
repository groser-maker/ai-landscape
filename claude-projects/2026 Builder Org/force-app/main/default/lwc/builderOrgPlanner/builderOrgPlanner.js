import { LightningElement, track } from 'lwc';
import getAllPersons from '@salesforce/apex/OrgPersonController.getAllPersons';
import getTargetOrgNumber from '@salesforce/apex/OrgPersonController.getTargetOrgNumber';
import savePerson from '@salesforce/apex/OrgPersonController.savePerson';
import savePositions from '@salesforce/apex/OrgPersonController.savePositions';
import saveTargetNumber from '@salesforce/apex/OrgPersonController.saveTargetNumber';

const CANVAS_HEIGHT = 4000,
    CANVAS_WIDTH = 6000,
    DEPTH_START = 0,
    FIELD_MANAGER = 'Manager__c',
    FIELD_POS_X = 'PositionX__c',
    FIELD_POS_Y = 'PositionY__c',
    FIELD_ROLE = 'Role__c',
    FIELD_STATUS = 'Status__c',
    FIELD_SUBTYPE = 'SubType__c',
    FIELD_TYPE = 'Type__c',
    GRID_COL = 160,
    GRID_ROW = 80,
    GRID_START_X = 40,
    GRID_START_Y = 40,
    SCROLL_OFFSET = 100,
    ZERO = 0;

export default class BuilderOrgPlanner extends LightningElement {
    @track people = [];
    @track targetOrgNumber = ZERO;
    @track isLoading = true;

    canvasSurfaceStyle = `width: ${CANVAS_WIDTH}px; height: ${CANVAS_HEIGHT}px;`;
    rootDepth = DEPTH_START;

    get totalCount() { return this.people.length; }

    get rootNode() {
        return this.buildTree(null);
    }

    connectedCallback() {
        this.loadData();
    }

    loadData() {
        Promise.all([getAllPersons(), getTargetOrgNumber()])
            .then(([rawPeople, target]) => {
                this.targetOrgNumber = target || ZERO;
                const needsLayout = rawPeople.some(
                    person => !person[FIELD_POS_X] && !person[FIELD_POS_Y]
                );
                if (needsLayout) {
                    this.people = BuilderOrgPlanner.assignInitialPositions(rawPeople);
                    BuilderOrgPlanner.persistPositions(this.people);
                } else {
                    this.people = rawPeople.slice();
                }
                this.isLoading = false;
            })
            .catch(() => {
                this.isLoading = false;
            });
    }

    static assignInitialPositions(rawPeople) {
        const managerGroups = {},
            positioned = rawPeople.map(person => ({ ...person }));
        rawPeople.forEach(person => {
            const managerKey = person[FIELD_MANAGER] || 'root';
            if (!managerGroups[managerKey]) { managerGroups[managerKey] = []; }
            managerGroups[managerKey].push(person);
        });
        positioned.forEach(person => {
            const managerKey = person[FIELD_MANAGER] || 'root';
            person[FIELD_POS_X] = GRID_START_X + managerGroups[managerKey].findIndex(sib => sib.Id === person.Id) * GRID_COL;
            person[FIELD_POS_Y] = GRID_START_Y + Object.keys(managerGroups).indexOf(managerKey) * GRID_ROW;
        });
        return positioned;
    }

    static persistPositions(persons) {
        const updates = persons.map(person => ({
            [FIELD_POS_X]: person[FIELD_POS_X],
            [FIELD_POS_Y]: person[FIELD_POS_Y],
            Id: person.Id
        }));
        savePositions({ updates }).catch(() => {});
    }

    buildTree(managerId) {
        const directReports = this.people.filter(person => {
                if (managerId === null) { return !person[FIELD_MANAGER]; }
                return person[FIELD_MANAGER] === managerId;
            }),
            [root] = directReports;
        if (!root) { return null; }
        return { children: this.buildChildren(root.Id), person: root };
    }

    buildChildren(parentId) {
        const directReports = this.people.filter(person => person[FIELD_MANAGER] === parentId);
        return directReports.map(person => ({
            children: this.buildChildren(person.Id),
            person
        }));
    }

    handleTargetChange(event) {
        const { detail: newTarget } = event;
        this.targetOrgNumber = newTarget;
        saveTargetNumber({ target: newTarget }).catch(() => {});
    }

    handlePersonClick(event) {
        const { detail } = event,
            person = this.people.find(candidate => candidate.Id === detail.personId);
        if (!person) { return; }
        this.scrollCanvasTo(person[FIELD_POS_X], person[FIELD_POS_Y]);
    }

    scrollCanvasTo(posX, posY) {
        const scroll = this.template.querySelector('.canvas-scroll');
        if (!scroll) { return; }
        scroll.scrollTo({ behavior: 'smooth', left: posX - SCROLL_OFFSET, top: posY - SCROLL_OFFSET });
    }

    handleCardMove(event) {
        const { detail } = event,
            updated = this.people.map(person => {
                if (person.Id !== detail.id) { return person; }
                return { ...person, [FIELD_POS_X]: detail.posX, [FIELD_POS_Y]: detail.posY };
            });
        this.people = updated;
    }

    handleCardDrop(event) {
        const { detail } = event,
            updated = this.people.map(person => {
                if (person.Id !== detail.id) { return person; }
                return { ...person, [FIELD_POS_X]: detail.posX, [FIELD_POS_Y]: detail.posY };
            });
        this.people = updated;
        savePositions({ updates: [{ [FIELD_POS_X]: detail.posX, [FIELD_POS_Y]: detail.posY, Id: detail.id }] }).catch(() => {});
    }

    handlePersonEdit(event) {
        const { detail } = event,
            updated = this.people.map(person => {
                if (person.Id !== detail.id) { return person; }
                return { ...person, [FIELD_ROLE]: detail.role, [FIELD_STATUS]: detail.status, [FIELD_SUBTYPE]: detail.subType, [FIELD_TYPE]: detail.type };
            });
        this.people = updated;
        savePerson({ person: { [FIELD_ROLE]: detail.role, [FIELD_STATUS]: detail.status, [FIELD_SUBTYPE]: detail.subType, [FIELD_TYPE]: detail.type, Id: detail.id } }).catch(() => {});
    }

    handleAutoArrange() {
        const arranged = BuilderOrgPlanner.assignInitialPositions(this.people);
        this.people = arranged;
        BuilderOrgPlanner.persistPositions(arranged);
    }
}
